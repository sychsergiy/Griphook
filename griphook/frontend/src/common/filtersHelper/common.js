export function isEmpty(iterable) {
  return iterable.length === 0;
}

export function separateSelectedItems(items, selectedItemsIds) {
  let selectedItems = [];

  let restItems = items.filter(item => {
    if (selectedItemsIds.includes(item.id)) {
      selectedItems.push(item);
      return false;
    }
    return true;
  });
  return [selectedItems, restItems];
}
