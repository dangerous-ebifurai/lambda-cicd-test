# デフォルトのターゲットを設定
.DEFAULT_GOAL := help

# イメージ一覧
.PHONY: im
im: ## イメージ一覧を表示します
	sudo docker images -a

# イメージを削除
.PHONY: rmi
rmi: ## イメージを削除します
	sudo docker rmi `sudo docker images -a -q`

# NWコマンドを実行
.PHONY: nw
nw: ## NWコマンドを実行します
	sudo docker network $(filter-out $@,$(MAKECMDGOALS))

# Volumeコマンドを実行
.PHONY: vol
vol: ## Volumeコマンドを実行します
	sudo docker volume $(filter-out $@,$(MAKECMDGOALS))

# コンテナを起動
.PHONY: up
up: ## コンテナを起動します
	sudo docker compose up -d

# コンテナを停止
.PHONY: down
down: ## コンテナを停止します
	sudo docker compose down

# コンテナをビルド
.PHONY: build
build: ## コンテナをビルドします
	sudo docker compose build --no-cache

# コンテナのステータスを表示
.PHONY: ps
ps: ## コンテナのステータスを表示します
	sudo docker compose ps -a

# コンテナの再起動
.PHONY: restart
restart: ## コンテナの再起動をします
	sudo docker compose restart $(filter-out $@,$(MAKECMDGOALS))

# 特定のコンテナのログを表示
.PHONY: logs
logs: ## 特定のコンテナのログを表示します
	sudo docker compose logs $(filter-out $@,$(MAKECMDGOALS))

# 特定のコンテナでシェルを起動
.PHONY: exec
exec: ## 特定のコンテナでシェルを起動します
	sudo docker compose exec $(filter-out $@,$(MAKECMDGOALS))

# ヘルプを表示
.PHONY: help
help: ## 使用可能なコマンドを表示します
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

%:
	@:
