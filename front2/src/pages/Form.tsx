import React, { useEffect, useState } from "react";
import { DateRangePicker, RangeKeyDict, Range } from "react-date-range";
import "react-date-range/dist/styles.css";
import "react-date-range/dist/theme/default.css";

const getTimeDiff = (from: string, to: string) => {
    if (!from || !to) return "";
    const [fh, fm] = from.split(":").map(Number);
    const [th, tm] = to.split(":").map(Number);
    if (isNaN(fh) || isNaN(fm) || isNaN(th) || isNaN(tm)) return "";
    const fromMins = fh * 60 + fm;
    const toMins = th * 60 + tm;
    const diff = toMins - fromMins;
    if (diff === 0) return "No change";
    const sign = diff > 0 ? "+" : "-";
    const absDiff = Math.abs(diff);
    const hours = Math.floor(absDiff / 60);
    const mins = absDiff % 60;
    let parts = [];
    if (hours) parts.push(`${hours}h`);
    if (mins) parts.push(`${mins}m`);
    return `${sign}${parts.join(" ")} (${from} → ${to})`;
};

const selectButtonSvg =
    "url('data:image/svg+xml,%3csvg xmlns=%27http://www.w3.org/2000/svg%27 width=%2724px%27 height=%2724px%27 fill=%27rgb(73,115,156)%27 viewBox=%270 0 256 256%27%3e%3cpath d=%27M181.66,170.34a8,8,0,0,1,0,11.32l-48,48a8,8,0,0,1-11.32,0l-48-48a8,8,0,0,1,11.32-11.32L128,212.69l42.34-42.35A8,8,0,0,1,181.66,170.34Zm-96-84.68L128,43.31l42.34,42.35a8,8,0,0,0,11.32-11.32l-48-48a8,8,0,0,0-11.32,0l-48,48A8,8,0,0,0,85.66,85.66Z%27%3e%3c/path%3e%3c/svg%3e')";

// Fake API call, now accepts dates
const fetchJobs = async (startDate: string, endDate: string) => {
    await new Promise((res) => setTimeout(res, 300));
    // You can use the dates to filter jobs if needed
    return [
        { id: "1", name: "Carpenter", start: "08:00", end: "16:00" },
        { id: "2", name: "Electrician", start: "09:00", end: "17:00" },
        { id: "3", name: "Plumber", start: "07:30", end: "15:30" },
    ];
};

function formatDate(date: Date | undefined) {
    if (!date) return "";
    return date.toISOString().slice(0, 10);
}

const Form: React.FC = () => {
    // Date range state using react-date-range
    const [range, setRange] = useState<Range>(
        {
            startDate: new Date(),
            endDate: new Date(),
            key: "selection",
        },
    );
    const [dateTouched, setDateTouched] = useState(false);

    const [jobs, setJobs] = useState<{ id: string; name: string; start: string; end: string }[]>([]);
    const [selectedJob, setSelectedJob] = useState<string>("");
    const [start, setStart] = useState<string>("");
    const [end, setEnd] = useState<string>("");
    const [notes, setNotes] = useState<string>("");
    const [reason, setReason] = useState<string>("");
    const [autofilled, setAutofilled] = useState<{ start: string; end: string }>({ start: "", end: "" });
    const [touched, setTouched] = useState<{ start: boolean; end: boolean }>({ start: false, end: false });
    const [submitted, setSubmitted] = useState(false);

    // Extract formatted dates
    const startDate = formatDate(range.startDate);
    const endDate = formatDate(range.endDate);

    // Fetch jobs only after both dates are selected
    useEffect(() => {
        if (startDate && endDate) {
            fetchJobs(startDate, endDate).then(setJobs);
        } else {
            setJobs([]);
            setSelectedJob("");
        }
    }, [startDate, endDate]);

    // Autofill start/end when job is selected
    useEffect(() => {
        if (selectedJob) {
            const job = jobs.find(j => j.id === selectedJob);
            if (job) {
                setStart(job.start);
                setEnd(job.end);
                setAutofilled({ start: job.start, end: job.end });
                setTouched({ start: false, end: false });
                setReason(""); // reset reason when job changes
            }
        } else {
            setStart("");
            setEnd("");
            setAutofilled({ start: "", end: "" });
            setTouched({ start: false, end: false });
            setReason("");
        }
    }, [selectedJob, jobs]);

    const startChanged = start !== autofilled.start;
    const endChanged = end !== autofilled.end;
    const reasonRequired = startChanged || endChanged;

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setSubmitted(true);
        if (!selectedJob) return;
        if (reasonRequired && !reason.trim()) return;
        alert("Form submitted!");
    };

    // Only show the rest of the form if both dates are selected
    const showFormFields = !!(startDate && endDate);

    return (
        <form
            onSubmit={handleSubmit}
            className="relative flex size-full min-h-screen flex-col bg-slate-50 justify-between group/design-root overflow-x-hidden"
            style={{
                // @ts-ignore
                "--select-button-svg": selectButtonSvg,
                fontFamily: 'Inter, "Noto Sans", sans-serif',
            }}
        >
            <div>
                {/* Date Range Picker */}
                <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                    <div className="flex flex-col min-w-40 flex-1">
                        <p className="text-[#0d141c] text-base font-medium leading-normal pb-2">
                            Date Range
                        </p>
                        <DateRangePicker
                            ranges={[range]}
                            onChange={(item: RangeKeyDict) => {
                                setRange(item.selection);
                                setDateTouched(true);
                            }}
                            minDate={new Date(new Date().setMonth(new Date().getMonth() - 1))}
                            maxDate={new Date()}
                            rangeColors={["#0c7ff2"]}
                        />
                    </div>
                </div>
                {submitted && (!startDate || !endDate) && (
                    <div className="text-red-500 text-xs pt-1 px-4">Both start and end dates are required</div>
                )}

                {/* Only show the rest if dates are picked */}
                {showFormFields && (
                    <>
                        <div className="flex items-center bg-slate-50 p-4 pb-2 justify-between">
                            <div
                                className="text-[#0d141c] flex size-12 shrink-0 items-center"
                                data-icon="X"
                                data-size="24px"
                                data-weight="regular"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="24px"
                                    height="24px"
                                    fill="currentColor"
                                    viewBox="0 0 256 256"
                                >
                                    <path d="M205.66,194.34a8,8,0,0,1-11.32,11.32L128,139.31,61.66,205.66a8,8,0,0,1-11.32-11.32L116.69,128,50.34,61.66A8,8,0,0,1,61.66,50.34L128,116.69l66.34-66.35a8,8,0,0,1,11.32,11.32L139.31,128Z" />
                                </svg>
                            </div>
                            <h2 className="text-[#0d141c] text-lg font-bold leading-tight tracking-[-0.015em] flex-1 text-center pr-12">
                                Submit Form
                            </h2>
                        </div>
                        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                            <label className="flex flex-col min-w-40 flex-1">
                                <select
                                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border-none bg-[#e7edf4] focus:border-none h-14 bg-[image:var(--select-button-svg)] placeholder:text-[#49739c] p-4 text-base font-normal leading-normal"
                                    value={selectedJob}
                                    onChange={e => setSelectedJob(e.target.value)}
                                    required
                                >
                                    <option value="" disabled>
                                        Select Job
                                    </option>
                                    {jobs.map((job) => (
                                        <option key={job.id} value={job.id}>
                                            {job.name}
                                        </option>
                                    ))}
                                </select>
                                {submitted && !selectedJob && (
                                    <span className="text-red-500 text-xs pt-1">Job is required</span>
                                )}
                            </label>
                        </div>
                        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                            <label className="flex flex-col min-w-40 flex-1">
                                <p className="text-[#0d141c] text-base font-medium leading-normal pb-2">
                                    Start Time
                                </p>
                                <input
                                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border-none bg-[#e7edf4] focus:border-none h-14 placeholder:text-[#49739c] p-4 text-base font-normal leading-normal"
                                    value={start}
                                    onChange={e => {
                                        setStart(e.target.value);
                                        setTouched(t => ({ ...t, start: true }));
                                    }}
                                    disabled={!selectedJob}
                                    placeholder="Start Time"
                                />
                                {startChanged && (
                                    <span className="text-yellow-600 text-xs pt-1">
                                        Original: {autofilled.start} &nbsp;|&nbsp; Diff: {getTimeDiff(autofilled.start, start)}. Please justify the change in the section below.
                                    </span>
                                )}
                            </label>
                        </div>
                        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                            <label className="flex flex-col min-w-40 flex-1">
                                <p className="text-[#0d141c] text-base font-medium leading-normal pb-2">
                                    End Time
                                </p>
                                <input
                                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border-none bg-[#e7edf4] focus:border-none h-14 placeholder:text-[#49739c] p-4 text-base font-normal leading-normal"
                                    value={end}
                                    onChange={e => {
                                        setEnd(e.target.value);
                                        setTouched(t => ({ ...t, end: true }));
                                    }}
                                    disabled={!selectedJob}
                                    placeholder="End Time"
                                />
                                {endChanged && (
                                    <span className="text-yellow-600 text-xs pt-1">
                                        Original: {autofilled.end} &nbsp;|&nbsp; Diff: {getTimeDiff(autofilled.end, end)}
                                    </span>
                                )}
                            </label>
                        </div>
                        {reasonRequired && (
                            <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                                <label className="flex flex-col min-w-40 flex-1">
                                    <textarea
                                        placeholder="Reason for changing start/end time"
                                        className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border-none bg-[#e7edf4] focus:border-none min-h-24 placeholder:text-[#49739c] p-4 text-base font-normal leading-normal"
                                        value={reason}
                                        onChange={e => setReason(e.target.value)}
                                        disabled={!selectedJob}
                                        required={reasonRequired}
                                    ></textarea>
                                    {submitted && reasonRequired && !reason.trim() && (
                                        <span className="text-red-500 text-xs pt-1">Reason is required if you change start/end time</span>
                                    )}
                                </label>
                            </div>
                        )}
                        <div className="flex max-w-[480px] flex-wrap items-end gap-4 px-4 py-3">
                            <label className="flex flex-col min-w-40 flex-1">
                                <textarea
                                    placeholder="Additional Notes (optional)"
                                    className="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-lg text-[#0d141c] focus:outline-0 focus:ring-0 border-none bg-[#e7edf4] focus:border-none min-h-36 placeholder:text-[#49739c] p-4 text-base font-normal leading-normal"
                                    value={notes}
                                    onChange={e => setNotes(e.target.value)}
                                    disabled={!selectedJob}
                                    required={false}
                                ></textarea>
                            </label>
                        </div>
                    </>
                )}
            </div>
            {showFormFields && (
                <div>
                    <div className="flex px-4 py-3">
                        <button
                            className="flex min-w-[84px] max-w-[480px] cursor-pointer items-center justify-center overflow-hidden rounded-lg h-12 px-5 flex-1 bg-[#0c7ff2] text-slate-50 text-base font-bold leading-normal tracking-[0.015em]"
                            type="submit"
                            disabled={!selectedJob}
                        >
                            <span className="truncate">Submit</span>
                        </button>
                    </div>
                    <div className="h-5 bg-slate-50"></div>
                </div>
            )}
        </form>
    );
};

export default Form;
