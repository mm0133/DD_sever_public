import React from 'react';
import ReactDOM from 'react-dom';
import * as serviceWorker from './serviceWorker';
import Root from './client/Root';
import './index.css';

ReactDOM.render(<Root/>, document.getElementById('root'));
serviceWorker.unregister();
