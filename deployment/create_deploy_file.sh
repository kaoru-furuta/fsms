# 既存ファイルがあれば削除
rm deploy.zip

# 最新のリポジトリをクローン
git clone git@github.com:kaoru-furuta/fsms.git fsms_deploy_dir

# アプリケーションディレクトリに移動
cd fsms_deploy_dir/apps/

# requirements.txt を同階層にコピーしてくる
cp ../requirements.txt .

# AWS 用の .env を作成する
cp .env.aws .env

# 必要なファイルを全て圧縮する
zip -r ../../deploy.zip * .env .ebextensions

# 最初の階層に戻る
cd ../../

# 作業用ディレクトリを削除
rm -rf fsms_deploy_dir
