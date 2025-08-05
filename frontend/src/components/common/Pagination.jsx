const Pagination = ({ page, limit, total, onPageChange }) => (
  <div className="flex justify-between items-center mt-4">
    <button disabled={page === 1} onClick={() => setPage(page - 1)}>
      قبلی
    </button>

    <button
      disabled={page >= Math.ceil(total / limit)}
      onClick={() => setPage(page + 1)}
    >
      بعدی
    </button>
  </div>
);

export default Pagination;
