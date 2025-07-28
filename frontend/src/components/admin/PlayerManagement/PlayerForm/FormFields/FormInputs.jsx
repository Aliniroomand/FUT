
export const InputField = ({ label, type = "text", ...props }) => (
  <div className="mb-4">
    <label className="block text-sm font-medium text-gray-300 mb-1">
      {label}
    </label>
    {type === "select" ? (
      <select
        className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
        {...props}
      >
        {props.children}
      </select>
    ) : (
      <input
        type={type}
        className="w-full p-2 rounded bg-white/30 backdrop-blur-md border border-gray-600 text-white focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
        {...props}
      />
    )}
  </div>
);

export const CheckboxField = ({ label, ...props }) => (
  <label className="flex items-center gap-2 text-sm text-gray-300 mb-4">
    <input
      type="checkbox"
      className="rounded bg-white/30 backdrop-blur-md border-gray-600 text-amber-600 focus:ring-amber-500"
      {...props}
    />
    {label}
  </label>
);