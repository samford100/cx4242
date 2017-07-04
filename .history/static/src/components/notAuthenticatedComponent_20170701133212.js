import React, {Component} from 'react';
import {connect} from 'react-redux';
import {bindActionCreators} from 'redux';
import {withRouter} from 'react-router';
import * as actionCreators from '../actions/auth';

function mapStateToProps(state) {
  return {token: state.auth.token, userName: state.auth.userName, isAuthenticated: state.auth.isAuthenticated};
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators(actionCreators, dispatch);
}

export function requireNoAuthentication(Component) {
  return <notAuthenticatedComponent Component={Component}/>
}

class notAuthenticatedComponent extends Component {

  constructor(props) {
    super(props);
    this.state = {
      loaded: false
    };
  }

  componentWillMount() {
    this.checkAuth();
  }

  componentWillReceiveProps(nextProps) {
    this.checkAuth(nextProps);
  }

  checkAuth(props = this.props) {
    if (props.isAuthenticated) {
      this
        .props
        .history
        .push('/main');

    } else {
      const token = localStorage.getItem('token');
      if (token) {
        fetch('api/is_token_valid', {
          method: 'post',
          credentials: 'include',
          headers: {
            'Accept': 'application/json', // eslint-disable-line quote-props
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({token})
        }).then(res => {
          if (res.status === 200) {
            this
              .props
              .loginUserSuccess(token);
            this
              .props
              .history
              .push('/main');

          } else {
            this.setState({loaded: true});
          }
        });
      } else {
        this.setState({loaded: true});
      }
    }
  }

  render() {
    console.log(this)
    return (
      <div>
        {!this.props.isAuthenticated && this.state.loaded
          ? <Component {...this.props}/>
          : null
}
      </div>
    );

  }
}

notAuthenticatedComponent.propTypes = {
  loginUserSuccess: React.PropTypes.func,
  isAuthenticated: React.PropTypes.bool
};

notAuthenticatedComponent withRouter(connect(mapStateToProps, mapDispatchToProps)(notAuthenticatedComponent));