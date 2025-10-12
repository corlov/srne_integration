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
                deviceId: action.payload.deviceId,
                expiresIn: action.payload.exp,
                role: action.payload.role
            };
        case 'LOGOUT':
            return {
                ...state,
                isAuthenticated: false,
                username: null,
                deviceId: null,
                expiresIn: null,
                role: null
            };
        default:
            return state;
    }
};

export default authReducer;