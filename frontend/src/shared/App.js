import React, {Component} from "react";
import {Route} from "react-router-dom";

import Header from "../components/Header";
import {Home, ContestList, ContestDetail} from "../pages";

class App extends Component {
    render() {
        return (
            <div>
                <Header/>
                <Route exact path="/" component={Home}/>
                <Route exact path="/contest" component={ContestList}/>
                <Route path="/contest/:id/overview" component={ContestDetail}/>
            </div>
        );
    }
}

export default App;