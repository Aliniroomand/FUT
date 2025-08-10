
const ToggleButton = ({ value, onChange }) => {
  return (
    <button
      onClick={() => onChange(!value)}
      className={`px-4 py-1 rounded-full font-semibold transition ${
        value ? "bg-green-500 text-white" : "bg-red-500 text-white"
      }`}
    >
      {value ? "بله" : "خیر"}
    </button>
  );
};

export default ToggleButton;
