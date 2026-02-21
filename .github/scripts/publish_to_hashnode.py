import os
import sys
import requests
import frontmatter
import re

HASHNODE_API_URL = "https://gql.hashnode.com"
HASHNODE_PAT = os.getenv('HASHNODE_PAT')
PUBLICATION_ID = os.getenv('HASHNODE_PUBLICATION_ID')
GITHUB_REPO = os.getenv('GITHUB_REPO')
GITHUB_BRANCH = os.getenv('GITHUB_BRANCH', 'main')
HASHNODE_BLOG_HOST = os.getenv('HASHNODE_BLOG_HOST') # 새로 추가된 변수

# --- GraphQL 쿼리 모음 ---
GET_POSTS_QUERY = """
query getPosts($host: String!) {
  publication(host: $host) {
    posts(first: 50) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
}
"""

CREATE_POST_MUTATION = """
mutation publishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      title
      url
    }
  }
}
"""

UPDATE_POST_MUTATION = """
mutation updatePost($input: UpdatePostInput!) {
  updatePost(input: $input) {
    post {
      id
      title
      url
    }
  }
}
"""

def extract_title_from_markdown(content, fallback_title):
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        new_content = re.sub(r'^#\s+(.+)$\n+', '', content, count=1, flags=re.MULTILINE)
        return title, new_content
    return fallback_title, content

def fix_image_urls(content, file_dir):
    pattern = r'!\[([^\]]*)\]\((?!http)(.*?)\)'
    def replace_url(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{file_dir}/{img_path}"
        return f"![{alt_text}]({raw_url})"
    return re.sub(pattern, replace_url, content)

def generate_tags_from_path(topic_folder):
    raw_tags = topic_folder.replace('-learn', '').split('-')
    raw_tags.append('TIL')
    tags = [{"slug": tag.lower(), "name": tag} for tag in raw_tags if tag]
    return tags

def main():
    filepath = sys.argv[1]
    
    if not os.path.exists(filepath):
        print(f"File {filepath} was deleted. Skipping.")
        sys.exit(0)

    path_parts = filepath.split('/')
    file_dir = os.path.dirname(filepath)
    
    topic_folder = path_parts[0] if len(path_parts) > 1 else "misc"
    chapter_folder = path_parts[1] if len(path_parts) > 2 else "Uncategorized"

    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    tags = post.get('tags')
    if tags:
        tag_objects = [{"slug": tag.lower().replace(" ", "-"), "name": tag} for tag in tags]
    else:
        tag_objects = generate_tags_from_path(topic_folder)

    content = post.content
    content = fix_image_urls(content, file_dir)

    title = post.get('title')
    if not title:
        fallback_title = f"[{topic_folder.replace('-learn', '').upper()}] {chapter_folder}"
        title, content = extract_title_from_markdown(content, fallback_title)

    headers = {
        "Authorization": HASHNODE_PAT
    }

    # --- 추가된 핵심 로직: 기존 글 검색 ---
    existing_post_id = None
    if HASHNODE_BLOG_HOST:
        posts_resp = requests.post(
            HASHNODE_API_URL,
            json={'query': GET_POSTS_QUERY, 'variables': {'host': HASHNODE_BLOG_HOST}},
            headers=headers
        ).json()
        
        # 제목이 똑같은 글이 있는지 검사
        if 'data' in posts_resp and posts_resp['data']['publication']:
            recent_posts = posts_resp['data']['publication']['posts']['edges']
            for edge in recent_posts:
                if edge['node']['title'] == title:
                    existing_post_id = edge['node']['id']
                    break

    # API 변수 세팅
    variables = {
        "input": {
            "title": title,
            "contentMarkdown": content,
            "publicationId": PUBLICATION_ID,
            "tags": tag_objects
        }
    }

    # 기존 글이 있으면 UPDATE, 없으면 CREATE
    if existing_post_id:
        print(f"🔄 Found existing post. Updating: {title}")
        variables["input"]["id"] = existing_post_id
        graphql_query = UPDATE_POST_MUTATION
    else:
        print(f"📝 Publishing new post: {title}")
        graphql_query = CREATE_POST_MUTATION

    response = requests.post(
        HASHNODE_API_URL,
        json={'query': graphql_query, 'variables': variables},
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"HTTP Error: {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()
    if 'errors' in result:
        print(f"GraphQL Error: {result['errors']}")
        sys.exit(1)

    # 응답 데이터 파싱 (updatePost인지 publishPost인지에 따라 다름)
    mutation_name = 'updatePost' if existing_post_id else 'publishPost'
    post_url = result['data'][mutation_name]['post']['url']
    print(f"✅ Success! URL: {post_url}")

if __name__ == "__main__":
    main()