module.exports = {
  apps: [{
    name: 'sensor',
    cmd: 'main.py',
    autorestart: true,
    watch: 'main.py',
    interpreter: '/usr/bin/python3'
  }]
};