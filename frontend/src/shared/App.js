import React, {Component} from "react";
import {Route} from "react-router-dom";

import Header from "../components/Header";
import {Home, ContestList, ContestDetail} from "../pages";
import Footer from "../components/Footer";

class App extends Component {
    render() {
        return (
            <div>
                <Header/>
                <Route exact path="/" component={Home}/>
                <Route exact path="/contest" component={ContestList}/>
                <Route path="/contest/:id/:type" component={ContestDetail}/>
                <Footer/>
            </div>
        );
    }
}

export default App;