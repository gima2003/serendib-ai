export default function CancellationProcessingModal({
    isOpen
}) {

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">

            <div className="bg-white rounded-3xl p-8 max-w-md w-full mx-4 shadow-xl text-center">

                <div className="text-5xl mb-4">
                    ⏳
                </div>

                <h2 className="text-2xl font-bold text-[#1C1917] mb-3">
                    Cancelling your Premium plan...
                </h2>

                <p className="text-[#78716C] mb-6">
                    Please wait while we process your cancellation.
                </p>

                <div className="flex justify-center">
                    <div className="w-8 h-8 border-4 border-orange-200 border-t-orange-500 rounded-full animate-spin"></div>
                </div>

            </div>

        </div>
    );
}