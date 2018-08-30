export const getErrorInformation = (errorData) => {
    let error = 'Error information: ';
    errorData.forEach((item) => {(error += item.msg + "; ")});
    return error
};