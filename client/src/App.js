import React, { Component }  from 'react';
import { Provider } from 'react-redux';
import store from './store';
import { BasePage } from './pages/BasePage';

function App() {
  return (
    <Provider store={store}>
      <BasePage />
    </Provider>
    
  );
}

export default App;
