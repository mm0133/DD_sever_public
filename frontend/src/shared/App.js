import React from "react";
import {Route, Switch} from "react-router-dom";
import Basic from "../pages/Basic";
import Auth from "../pages/Auth";

const App = () => {
    return (
        <div>
            <Switch>
                <Route path="/auth" component={Auth} />
                <Route path="/" component={Basic}/>
            </Switch>
        </div>
    );
}

export default App;