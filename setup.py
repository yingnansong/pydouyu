from distutils.core import setup
setup(
  name = 'douyu',
  packages = ['douyu', 'douyu.chat', 'douyu.chat.network'],
  version = '0.1.2',
  description = 'Python Wrapper for DouyuTV APIs, including support for accessing ChatRoom, e.g. DanMu',
  author = 'Yingnan Song',
  author_email = 'syngod12345@gmail.com',
  url = 'https://github.com/yingnansong/pydouyu',
  download_url = 'https://github.com/yingnansong/pydouyu/tarball/0.1.2',
  keywords = ['douyu', 'douyutv', 'danmu', 'chat'],
  classifiers = [],
)