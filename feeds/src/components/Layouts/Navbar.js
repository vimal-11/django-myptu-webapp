import React, { useState, useEffect, Component } from 'react';
import { AppBar, Typography, Toolbar, Button } from '@material-ui/core';
import { Link } from 'react-router-dom';




import useStyles from './styles.js';

class Navbar extends Component  {
   
  render(){
    const classes = useStyles();
  
  return (
    <AppBar className={classes.appBar} position="static" color="inherit">
      <div className={classes.brandContainer}>
        <Typography component={Link} to="/" className={classes.heading} variant="h2" align="center">Memories</Typography>
      
      </div>
      <Toolbar className={classes.toolbar}>
      
          <div className={classes.profile}>
      
            <Typography className={classes.userName} variant="h6">Username</Typography>
            <Button variant="contained" className={classes.logout} color="secondary" onClick={logout}>Logout</Button>
          </div>
   
          <Button component={Link} to="/auth" variant="contained" color="primary">Sign In</Button>
  
      </Toolbar>
    </AppBar>
  );
        }
}

export default Navbar;

