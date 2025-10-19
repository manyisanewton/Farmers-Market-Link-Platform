export default {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapper: {
    '\\.css$': 'identity-obj-proxy',
  },
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleFileExtensions: ['js', 'jsx'],
  testMatch: ['**/?(*.)+(test).[jt]s?(x)'],
};
