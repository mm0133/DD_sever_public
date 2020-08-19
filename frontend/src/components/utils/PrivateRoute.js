// This is used to determine if a user is authenticated and
// if they are allowed to visit the page they navigated to.

// If they are: they proceed to the page
// If not: they are redirected to the login page.
import React, {useEffect, useState} from 'react'
import {Redirect, Route} from 'react-router-dom'
import {getTokenAndExpire} from "../../apis/config";

const PrivateRoute = ({component: Component, ...rest}) => {
    const [isLoggedIn, setIsLoggedIn] = useState(true);
    useEffect(() => {
        const wow = async () => {
            const {token, expireDateTime} = await getTokenAndExpire();
            // expireDateTime 이 null 이면 두번째 조건문에서 error 가 뜬다.
            if (!(token && Date.now() < expireDateTime)) {
                setIsLoggedIn(false);
            }
        }
        wow();
    }, [])

    return (
        <Route
            {...rest}
            render={props =>
                isLoggedIn ? (
                    <Component {...props} />
                ) : (
                    <Redirect to={{pathname: '/auth/login', state: {from: props.location}}}/>
                )
            }
        />
    )
}

export default PrivateRoute