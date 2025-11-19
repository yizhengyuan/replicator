"use client";

import { useState, useEffect, useRef } from "react";
import { Play, Pause, RotateCcw, Coffee, Brain, Timer } from "lucide-react";
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: (string | undefined | null | false)[]) {
  return twMerge(clsx(inputs));
}

type TimerMode = "pomodoro" | "shortBreak" | "longBreak";

const MODES: Record<TimerMode, { label: string; minutes: number; color: string }> = {
  pomodoro: { label: "Pomodoro", minutes: 25, color: "bg-red-500" },
  shortBreak: { label: "Short Break", minutes: 5, color: "bg-teal-500" },
  longBreak: { label: "Long Break", minutes: 15, color: "bg-blue-500" },
};

export default function PomodoroTimer() {
  const [mode, setMode] = useState<TimerMode>("pomodoro");
  const [timeLeft, setTimeLeft] = useState(MODES.pomodoro.minutes * 60);
  const [isActive, setIsActive] = useState(false);
  const [progress, setProgress] = useState(100);

  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const currentMode = MODES[mode];

  useEffect(() => {
    if (isActive && timeLeft > 0) {
      timerRef.current = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsActive(false);
      if (timerRef.current) clearInterval(timerRef.current);
      // In a real app, we'd play a sound here
    }

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isActive, timeLeft]);

  useEffect(() => {
    const totalSeconds = currentMode.minutes * 60;
    setProgress((timeLeft / totalSeconds) * 100);
  }, [timeLeft, currentMode.minutes]);

  const toggleTimer = () => setIsActive(!isActive);

  const resetTimer = () => {
    setIsActive(false);
    setTimeLeft(currentMode.minutes * 60);
  };

  const switchMode = (newMode: TimerMode) => {
    setMode(newMode);
    setIsActive(false);
    setTimeLeft(MODES[newMode].minutes * 60);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  return (
    <div className={cn("min-h-screen transition-colors duration-500 flex items-center justify-center p-4",
      mode === "pomodoro" ? "bg-red-50" : mode === "shortBreak" ? "bg-teal-50" : "bg-blue-50"
    )}>
      <div className="max-w-md w-full">
        {/* Header */}
        <div className="flex items-center justify-center gap-2 mb-8 text-slate-700">
          <Timer size={32} className={cn("transition-colors duration-500",
            mode === "pomodoro" ? "text-red-500" : mode === "shortBreak" ? "text-teal-500" : "text-blue-500"
          )} />
          <h1 className="text-3xl font-bold tracking-tight">Focus Flow</h1>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-slate-100">
          {/* Mode Switcher */}
          <div className="flex p-2 bg-slate-100/50 gap-1 m-2 rounded-2xl">
            {(Object.keys(MODES) as TimerMode[]).map((m) => (
              <button
                key={m}
                onClick={() => switchMode(m)}
                className={cn(
                  "flex-1 py-2 px-4 rounded-xl text-sm font-medium transition-all duration-300",
                  mode === m
                    ? cn("bg-white shadow-sm text-slate-800",
                      m === "pomodoro" ? "text-red-600" : m === "shortBreak" ? "text-teal-600" : "text-blue-600")
                    : "text-slate-500 hover:text-slate-700 hover:bg-slate-200/50"
                )}
              >
                {MODES[m].label}
              </button>
            ))}
          </div>

          {/* Timer Display */}
          <div className="p-12 flex flex-col items-center">
            <div className="relative mb-12">
              {/* Progress Ring Background */}
              <div className="w-64 h-64 rounded-full border-8 border-slate-100 flex items-center justify-center">
                <div className="text-center">
                  <div className={cn("text-7xl font-bold tabular-nums tracking-tighter transition-colors duration-500",
                    mode === "pomodoro" ? "text-red-600" : mode === "shortBreak" ? "text-teal-600" : "text-blue-600"
                  )}>
                    {formatTime(timeLeft)}
                  </div>
                  <div className="text-slate-400 font-medium mt-2 uppercase tracking-widest text-sm">
                    {isActive ? "Focusing" : "Paused"}
                  </div>
                </div>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center gap-6">
              <button
                onClick={toggleTimer}
                className={cn(
                  "h-20 w-20 rounded-2xl flex items-center justify-center text-white shadow-lg hover:shadow-xl hover:scale-105 active:scale-95 transition-all duration-300",
                  currentMode.color
                )}
              >
                {isActive ? <Pause size={32} fill="currentColor" /> : <Play size={32} fill="currentColor" className="ml-1" />}
              </button>

              <button
                onClick={resetTimer}
                className="h-14 w-14 rounded-xl bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700 flex items-center justify-center transition-all duration-200"
              >
                <RotateCcw size={24} />
              </button>
            </div>
          </div>
        </div>

        {/* Footer / Tips */}
        <div className="mt-8 text-center text-slate-500 text-sm">
          <p className="flex items-center justify-center gap-2">
            {mode === "pomodoro" ? (
              <>
                <Brain size={16} />
                <span>Time to focus! Eliminate distractions.</span>
              </>
            ) : (
              <>
                <Coffee size={16} />
                <span>Take a deep breath. Relax.</span>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
