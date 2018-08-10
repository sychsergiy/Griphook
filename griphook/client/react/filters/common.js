export const ITEMS_PER_FILTER_PAGE = 5;

export function isEmpty(iterable) {
  return iterable.length === 0;
}

export function separateSelectedItems(items, selectedItemsIds) {
  let selectedItems = [];

  let restItems = items.filter(item => {
    if (selectedItemsIds.includes("" + item.id)) {
      selectedItems.push(item);
      return false;
    }
    return true;
  });
  return [selectedItems, restItems];
}

export function paginator(items, itemsPerPage = ITEMS_PER_FILTER_PAGE) {
  function getPage(pageNumber) {
    const startIndex = pageNumber * itemsPerPage;
    const endIndex = (pageNumber + 1) * itemsPerPage;
    const slicedItems = items.slice(startIndex, endIndex);

    function nextPageExists() {
      return endIndex >= items.length ? false : true;
    }

    function previousPageExists() {
      return startIndex <= 0 ? false : true;
    }

    return { items: slicedItems, nextPageExists, previousPageExists };
  }
  return { getPage };
}
