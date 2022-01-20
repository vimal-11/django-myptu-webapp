import React,{Component} from "react";
import {Router, Route,Switch} from "react-router";
import ReactDOM  from "react-dom";
import Navbar from "./Layouts/Navbar.js";
import {createBrowserHistory} from 'history';

class App extends Component {
    render() {
        return (
            <div>
                <Router history={history}>
                <Switch>
                    <Route exact path="/Home" component={Navbar}/>
                </Switch>
                </Router>
            </div>
        
        );
    }
}

ReactDOM.render(<App />,document.getElementById('app'));

