# AWS LambdaのPython3.11ベースイメージ
FROM public.ecr.aws/lambda/python:3.11

# 必要なパッケージをインストール
RUN yum install -y zip

# 作業ディレクトリを設定
WORKDIR /var/task

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --target . -r requirements.txt

# Lambda ハンドラーのコードをコピー
COPY index.py ./

# Lambda の起動コマンド
CMD ["index.lambda_handler"]
