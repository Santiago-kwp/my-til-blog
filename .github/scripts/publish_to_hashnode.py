# file: .github/scripts/publish_to_hashnode.py

import os
import sys
import requests
import frontmatter # frontmatter를 파싱하기 위한 라이브러리

# --- 설정 값 ---
HASHNODE_API_URL = "https://gql.hashnode.com"
# GitHub Secrets에서 값들을 가져옵니다.
HASHNODE_PAT = os.getenv('HASHNODE_PAT')
PUBLICATION_ID = os.getenv('HASHNODE_PUBLICATION_ID')

# --- GraphQL 쿼리 ---
# Hashnode에 새 글을 발행하기 위한 Mutation
CREATE_POST_MUTATION = """
mutation publishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      id
      title
      slug
      url
    }
  }
}
"""

def main():
    # 워크플로우에서 변경된 파일의 경로를 인자로 받습니다.
    filepath = sys.argv[1]

    # 파일이 존재하지 않으면 오류를 발생시킵니다.
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        sys.exit(1)

    # 마크다운 파일과 frontmatter를 읽어옵니다.
    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    # 메타데이터(필수)와 본문(content)을 추출합니다.
    title = post.get('title')
    content = post.content # frontmatter를 제외한 순수 마크다운 내용
    tags = post.get('tags', []) # 태그는 선택사항

    # 필수 메타데이터 확인
    if not title:
        print(f"Error: 'title' not found in frontmatter of {filepath}")
        sys.exit(1)

    # 태그를 Hashnode API 형식에 맞게 변환합니다.
    # 예: ['python', 'github'] -> [{"slug": "python", "name": "python"}, {"slug": "github", "name": "github"}]
    tag_objects = [{"slug": tag.lower().replace(" ", "-"), "name": tag} for tag in tags]

    # API에 보낼 변수들을 정의합니다.
    variables = {
        "input": {
            "title": title,
            "contentMarkdown": content,
            "publicationId": PUBLICATION_ID,
            "tags": tag_objects
        }
    }

    # API 요청 헤더
    headers = {
        "Authorization": HASHNODE_PAT
    }

    # API 요청 실행
    try:
        response = requests.post(
            HASHNODE_API_URL,
            json={'query': CREATE_POST_MUTATION, 'variables': variables},
            headers=headers
        )
        response.raise_for_status() # HTTP 오류가 있으면 예외 발생

        result = response.json()

        # API 응답에 오류가 있는지 확인
        if 'errors' in result:
            print(f"GraphQL Error: {result['errors']}")
            sys.exit(1)

        post_data = result['data']['publishPost']['post']
        print(f"✅ Successfully published post to Hashnode!")
        print(f"   - Title: {post_data['title']}")
        print(f"   - URL: {post_data['url']}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        print(f"Response: {response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()