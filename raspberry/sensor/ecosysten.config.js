module.exports = {
  apps: [{
    name: 'sensor',
    cmd: 'main.py',
    autorestart: true,
    watch: true,
    interpreter: '/usr/bin/python3'
  }]
};