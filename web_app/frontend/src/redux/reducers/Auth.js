const initialState = {
    isAuthenticated: false,
    username: null,
};

const authReducer = (state = initialState, action) => {
    switch (action.type) {
        case 'LOGIN':
            return {
                ...state,
                isAuthenticated: true,
                username: action.payload.username,
                loginTimestamp: action.payload.loginTimestamp,
                token: action.payload.token,
            };
        case 'LOGOUT':
            return {
                ...state,
                isAuthenticated: false,
                username: null,
            };
        default:
            return state;
    }
};

export default authReducer;