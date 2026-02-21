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

def extract_title_from_markdown(content, fallback_title):
    """마크다운 본문에서 첫 번째 # 제목을 추출합니다."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        # 본문에서 # 제목 줄을 제거하고, 제목만 반환
        title = match.group(1).strip()
        new_content = re.sub(r'^#\s+(.+)$\n+', '', content, count=1, flags=re.MULTILINE)
        return title, new_content
    return fallback_title, content

def fix_image_urls(content, file_dir):
    """로컬 이미지 경로를 GitHub Raw URL로 변환합니다."""
    # ![alt](경로) 형태를 찾습니다. (http로 시작하는 웹 URL은 무시)
    pattern = r'!\[([^\]]*)\]\((?!http)(.*?)\)'
    
    def replace_url(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        # GitHub Raw URL 생성
        # 예: https://raw.githubusercontent.com/Santiago-kwp/TIL/main/opencv-python-learn/Chap4.../images/sample.png
        raw_url = f"https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_BRANCH}/{file_dir}/{img_path}"
        return f"![{alt_text}]({raw_url})"

    return re.sub(pattern, replace_url, content)

def generate_tags_from_path(topic_folder):
    """폴더명을 기반으로 Hashnode 태그 형식으로 변환합니다."""
    # 예: opencv-python-learn -> ['opencv', 'python']
    raw_tags = topic_folder.replace('-learn', '').split('-')
    raw_tags.append('TIL') # 기본 태그 추가
    
    # Hashnode는 tag slug 형식을 요구합니다.
    tags = [{"slug": tag.lower(), "name": tag} for tag in raw_tags if tag]
    return tags

def main():
    filepath = sys.argv[1]
    
    # 파일이 존재하는지 확인 (삭제된 파일 처리)
    if not os.path.exists(filepath):
        print(f"File {filepath} was deleted. Skipping.")
        sys.exit(0)

    # 경로 분석 (예: opencv-python-learn/Chap4-OpenCV.../README.md)
    path_parts = filepath.split('/')
    file_dir = os.path.dirname(filepath)
    
    topic_folder = path_parts[0] if len(path_parts) > 1 else "misc"
    chapter_folder = path_parts[1] if len(path_parts) > 2 else "Uncategorized"

    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # 1. 태그 설정 (Frontmatter가 있으면 쓰고, 없으면 폴더명 기반 생성)
    tags = post.get('tags')
    if tags:
        tag_objects = [{"slug": tag.lower().replace(" ", "-"), "name": tag} for tag in tags]
    else:
        tag_objects = generate_tags_from_path(topic_folder)

    # 2. 본문 가져오기 및 이미지 경로 수정
    content = post.content
    content = fix_image_urls(content, file_dir)

    # 3. 제목 설정 (Frontmatter -> 마크다운 # H1 -> 폴더명 순으로 탐색)
    title = post.get('title')
    if not title:
        fallback_title = f"[{topic_folder.replace('-learn', '').upper()}] {chapter_folder}"
        title, content = extract_title_from_markdown(content, fallback_title)

    variables = {
        "input": {
            "title": title,
            "contentMarkdown": content,
            "publicationId": PUBLICATION_ID,
            "tags": tag_objects
        }
    }

    headers = {
        "Authorization": HASHNODE_PAT
    }

    print(f"Uploading: {title}")
    
    response = requests.post(
        HASHNODE_API_URL,
        json={'query': CREATE_POST_MUTATION, 'variables': variables},
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

    post_url = result['data']['publishPost']['post']['url']
    print(f"✅ Successfully published! URL: {post_url}")

if __name__ == "__main__":
    main()