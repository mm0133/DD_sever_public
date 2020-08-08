import React, {Component} from "react";
import {Route} from "react-router-dom";

import Header from "../components/Header";
import {Home, ContestList, Posts, ContestDetail} from "../pages";

class App extends Component {
    render() {
        return (
            <div>
                <Header/>
                <Route exact path="/" component={Home}/>
                <Route exact path="/contest" component={ContestList}/>
                <Route path="/contest/:id" component={ContestDetail}/>
                <Route path="/posts" component={Posts}/>
            </div>
        );
    }
}

export default App;