const countReducer = (state = {value:0}, action) => {
  switch (action.type) {
    case "ADD_ONE":
      return {
        value: state.value + 1,
      };
    case "MINUS_ONE":
        return {
            ...state,
          value: state.value + 1,
        };
    default:
      return state;
  }
};

export default countReducer
