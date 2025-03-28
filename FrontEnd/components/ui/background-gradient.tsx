"use client"
import type React from "react"
import { cn } from "@/lib/utils"

export const BackgroundGradient = ({
  children,
  className,
  containerClassName,
  animate = true,
}: {
  children?: React.ReactNode
  className?: string
  containerClassName?: string
  animate?: boolean
}) => {
  const variants = {
    initial: {
      backgroundPosition: "0 50%",
    },
    animate: {
      backgroundPosition: ["0, 50%", "100% 50%", "0 50%"],
    },
  }
  return (
    <div className={cn("relative p-[4px] group", containerClassName)}>
      <div
        className={cn(
          "absolute inset-0 rounded-lg bg-gradient-to-r from-[#050A44] via-[#0A21C0] to-[#2C2E3A] group-hover:opacity-100 blur-xl transition duration-500",
          animate ? "animate-gradient" : "",
          className,
        )}
      />
      <div
        className={cn(
          "absolute inset-0 rounded-lg bg-gradient-to-r from-[#050A44] via-[#0A21C0] to-[#2C2E3A] group-hover:opacity-100",
          animate ? "animate-gradient" : "",
          className,
        )}
      />
      <div className="relative">{children}</div>
    </div>
  )
}

