import React from "react";
import {Route} from "react-router-dom";

import {Home, Header, Footer} from "../components/Basic";
import {ContestList, ContestDetail} from "../components/Contest";

const Basic = () => {
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

export default Basic;