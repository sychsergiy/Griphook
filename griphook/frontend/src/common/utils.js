export function isEquivalent(firstObject, secondObject) {
  let firstObjectProps = Object.getOwnPropertyNames(firstObject);
  let secondObjectProps = Object.getOwnPropertyNames(secondObject);

  if (firstObjectProps.length != secondObjectProps.length) {
    return false;
  }

  for (let i = 0; i < firstObjectProps.length; i++) {
    let propName = firstObjectProps[i];
    if (firstObject[propName] !== secondObject[propName]) {
      return false;
    }
  }
  return true;
}
