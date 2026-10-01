export default function SubscriptionCancellationModal({
    isOpen,
    onClose
}) {

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">

            <div className="bg-white rounded-3xl p-8 max-w-md w-full mx-4 shadow-xl text-center">

                <div className="text-5xl mb-4">
                    👋
                </div>

                <h2 className="text-2xl font-bold text-[#1C1917] mb-3">
                    Premium Subscription Cancelled
                </h2>

                <p className="text-[#78716C] mb-6">
                    Your Premium subscription has been cancelled successfully.
                    You can continue using Serendib AI with the Free plan.
                </p>

                <div className="text-left bg-orange-50 rounded-xl p-4 mb-6">

                    <p className="font-medium mb-2">
                        Free plan includes:
                    </p>

                    <ul className="text-sm space-y-1">

                        <li>
                            ✓ 3 AI consultations
                        </li>

                        <li>
                            ✓ 3 guided trip plans
                        </li>

                        <li>
                            ✓ Basic destination recommendations
                        </li>

                    </ul>

                </div>

                <button
                    onClick={onClose}
                    className="w-full bg-orange-500 text-white py-3 rounded-xl font-semibold hover:bg-orange-600"
                >
                    Continue Planning
                </button>

            </div>

        </div>
    );
}