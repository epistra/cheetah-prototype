# 環境構築メモ

```sh
mkdir -p server client
```

## Server

```sh
$ cd server
$ python3.6 -m venv env
$ source env/bin/activate
```

```sh
(env)$ pip install --upgrade pip
(env)$ pip install Flask==1.0.2 Flask-Cors==3.0.4
(env)$ pip install flask_sqlalchemy
(env)$ pip install Flask-Migrate
```

## Client

```sh
$ npm install -g vue-cli@2.9.6
$ vue init webpack client
```

| Setting Item                        | Value             |
|-------------------------------------|-------------------|
| Project name                        | cheetah-prot      |
| Project description                 | Cheetah Prototype |
| Author                              |                   |
| Vue build                           | standalone        |
| Install vue-router?                 | Yes               |
| Use ESLint to lint your code?       | Yes               |
| Pick an ESLint preset               | AirBnB            |
| Set up unit tests                   | No                |
| Setup e2e tests with Nightwatch?    | No                |
| Should we run `npm install` for ... | npm               |

```sh
$ cd client
$ npm install axios@0.18.0 --save
$ npm install vuetify --save
$ npm install material-design-icons --save
$ npm install moment --save
$ npm install vue-moment --save
$ npm install dayspan --save
$ npm install dayspan-vuetify --save
$ npm install sass-loader node-sass --save-dev
```
