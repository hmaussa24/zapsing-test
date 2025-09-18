const target = process.env.API_BASE_URL || 'http://localhost:8000';

module.exports = {
  '/api': {
    target,
    secure: false,
    changeOrigin: true,
    logLevel: 'debug',
  },
};


