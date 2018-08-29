export const ITEMS_PER_FILTER_PAGE = 8;

export function paginator(items, pageNumber, itemsPerPage = ITEMS_PER_FILTER_PAGE) {
  const endIndex = pageNumber * itemsPerPage;

  const amountAllPages =  Math.ceil(items.length / itemsPerPage)

  if (endIndex >= items.length && pageNumber > 1) {
    pageNumber = amountAllPages;
  }

  const startIndex = (pageNumber - 1) * itemsPerPage;
  const slicedItems = items.slice(startIndex, endIndex);

  const nextPageExists = endIndex < items.length;
  const previousPageExists = startIndex > 0;

  return {
    items: slicedItems,
    nextPageExists,
    previousPageExists,
    pageNumber,
    amountAllPages
  };
}
