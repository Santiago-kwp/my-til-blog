---
title: "GitHub Actions로 Hashnode 블로그 자동 포스팅 구축하기 (feat. 첫 자동 발행 성공!)"
tags:
  - "GitHub Actions"
  - "Automation"
  - "Hashnode"
  - "TIL"
  - "Python"
---

## 안녕하세요, Hashnode! 👋

이 글은 저의 GitHub TIL(Today I Learned) 레포지토리에 마크다운(`.md`) 파일을 푸시하면, **GitHub Actions가 이를 감지하여 자동으로 Hashnode 블로그에 글을 발행해 주는 시스템**을 통해 작성되었습니다.

원래는 티스토리(Tistory) API를 활용해 자동화를 하려고 했으나, 최근 티스토리 오픈 API가 완전히 종료됨에 따라 훌륭한 대안인 **Hashnode**를 선택하게 되었습니다. Hashnode는 개발자 친화적이며 강력한 GraphQL API를 제공하여 자동화 구축이 매우 수월합니다.

저처럼 GitHub 레포지토리를 블로그와 연동하여 자동으로 글을 업로드하고 싶으신 분들을 위해, 제가 방금 성공한 따끈따끈한 구축 방법을 단계별로 공유합니다!

---

## 🛠️ 1단계: Hashnode API 키 및 블로그 ID 발급

외부(GitHub)에서 내 Hashnode 블로그에 글을 쓰려면 권한이 필요합니다.

1. **Personal Access Token (PAT) 발급**
   - Hashnode 우측 상단 프로필 > `Account Settings` > `Developer` 메뉴로 이동합니다.
   - `Generate New Token`을 클릭하고 이름을 지정한 뒤 발급합니다.
   - **(중요)** 발급된 토큰은 다시 볼 수 없으니 반드시 복사해 둡니다.

2. **내 블로그의 Publication ID 확인**
   - [Hashnode GraphQL Playground](https://gql.hashnode.com/)에 접속합니다.
   - 좌측 쿼리창에 아래 코드를 입력하고 `your-blog.hashnode.dev` 부분을 본인의 블로그 주소로 변경합니다.
     ```graphql
     query {
       publication(host: "your-blog.hashnode.dev") {
         id
       }
     }
     ```
   - 상단의 재생(▶) 버튼을 누르면 우측에 `id` 값(예: `625d...`)이 나옵니다. 이 값을 복사합니다.

---

## 🔒 2단계: GitHub 레포지토리 Secrets 설정

발급받은 토큰과 ID를 코드에 직접 노출하면 안 되므로 GitHub Secrets에 안전하게 보관합니다.

1. 포스트를 관리할 GitHub 레포지토리의 `Settings` > `Secrets and variables` > `Actions`로 이동합니다.
2. `New repository secret`을 클릭하여 다음 두 가지를 추가합니다.
   - `HASHNODE_PAT`: 1단계에서 발급받은 PAT 토큰 값
   - `HASHNODE_PUBLICATION_ID`: 1단계에서 확인한 Publication ID 값

---

## 📁 3단계: 폴더 구조 설정

로컬 컴퓨터에 레포지토리를 클론하고 다음과 같은 폴더 구조를 만듭니다.

```text
my-til-blog/
├── .github/
│   ├── workflows/    # GitHub Actions 설정 파일이 들어갈 곳
│   └── scripts/      # 파이썬 자동화 스크립트가 들어갈 곳
└── _posts/           # 마크다운 포스트(.md)를 작성할 곳
```

---

## 🐍 4단계: 포스팅 파이썬 스크립트 작성

.github/scripts/ 폴더 안에 publish_to_hashnode.py 파일을 생성하고 아래 코드를 작성합니다. 이 스크립트는 마크다운 파일의 메타데이터(Frontmatter)와 본문을 읽어 Hashnode API로 전송하는 역할을 합니다.

```python
import os
import sys
import requests
import frontmatter

HASHNODE_API_URL = "https://gql.hashnode.com"
HASHNODE_PAT = os.getenv('HASHNODE_PAT')
PUBLICATION_ID = os.getenv('HASHNODE_PUBLICATION_ID')

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

def main():
    filepath = sys.argv[1]

    with open(filepath, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)

    title = post.get('title')
    content = post.content
    tags = post.get('tags', [])

    if not title:
        print(f"Error: 'title' not found in frontmatter of {filepath}")
        sys.exit(1)

    tag_objects = [{"slug": tag.lower().replace(" ", "-"), "name": tag} for tag in tags]

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

    response = requests.post(
        HASHNODE_API_URL,
        json={'query': CREATE_POST_MUTATION, 'variables': variables},
        headers=headers
    )
    response.raise_for_status()

    result = response.json()
    if 'errors' in result:
        print(f"GraphQL Error: {result['errors']}")
        sys.exit(1)

    print("✅ Successfully published post to Hashnode!")

if __name__ == "__main__":
    main()
```

---

## ⚙️ 5단계: GitHub Actions 워크플로우 작성

언제 위의 파이썬 스크립트를 실행할지 정의하는 파일입니다. .github/workflows/ 폴더 안에 publish_article.yml 파일을 만들고 아래 코드를 넣습니다.

```yaml
name: Publish to Hashnode

on:
  push:
    branches:
      - main
    paths:
      - "_posts/**.md"

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Find changed markdown files
        id: changed_files
        uses: tj-actions/changed-files@v35
        with:
          files: _posts/**.md

      - name: Set up Python
        if: steps.changed_files.outputs.any_changed == 'true'
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install Python Dependencies
        if: steps.changed_files.outputs.any_changed == 'true'
        run: |
          python -m pip install --upgrade pip
          pip install python-frontmatter requests

      - name: Run publisher script for each changed file
        if: steps.changed_files.outputs.any_changed == 'true'
        env:
          HASHNODE_PAT: ${{ secrets.HASHNODE_PAT }}
          HASHNODE_PUBLICATION_ID: ${{ secrets.HASHNODE_PUBLICATION_ID }}
        run: |
          for file in ${{ steps.changed_files.outputs.all_changed_files }}; do
            python .github/scripts/publish_to_hashnode.py "$file"
          done
```

---

## 📝 6단계: 글 작성 및 푸시

이제 `\_posts/` 폴더 안에 마크다운 파일을 만들고 글을 작성합니다. 파일의 최상단에는 반드시 아래와 같이 `---` 로 감싼 **Frontmatter**를 넣어주어야 스크립트가 제목과 태그를 인식합니다.

```markdown
---
title: "포스트 제목입니다"
tags:
  - "태그1"
  - "태그2"
---

본문 내용...
```

모두 작성했다면 GitHub에 커밋하고 푸시합니다!

---

## 💡 주의사항 (제가 겪은 시행착오!)

모든 설정을 마치고 **"첫 번째 커밋"**으로 모든 파일(스크립트 포함)을 올리면 워크플로우가 정상 완료되었다고 뜨는데 글은 안 올라가는 현상이 발생할 수 있습니다.
이는 우리가 사용한 tj-actions/changed-files 액션이 '이전 커밋'과 '현재 커밋'을 비교해서 변경된 파일을 찾기 때문입니다. 첫 커밋은 비교할 대상이 없어서 변경된 파일이 '0개'라고 판단하고 스크립트 실행을 건너뜁니다.
해결책: 마크다운 파일에 띄어쓰기 하나라도 수정한 뒤 두 번째 커밋을 푸시해 보세요. 그때부터는 정상적으로 변경 파일을 감지하고 블로그에 글이 촥촥 올라갑니다!
이제 잔디(Commit)도 심고 블로그 관리도 하는 일석이조의 효과를 누려보세요! 🚀

````
---

이제 터미널에서 아래 명령어를 순서대로 실행하시면 업데이트가 완료됩니다.

```bash
git add .
git commit -m "docs: Update first post with full tutorial"
git push origin main
````
