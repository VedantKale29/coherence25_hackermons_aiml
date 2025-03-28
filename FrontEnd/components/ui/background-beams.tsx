"use client"
import type React from "react"
import { useEffect, useRef, useState } from "react"
import { cn } from "@/lib/utils"

export const BackgroundBeams = ({
  className,
}: {
  className?: string
}) => {
  const [mousePosition, setMousePosition] = useState<{ x: number; y: number }>({
    x: 0,
    y: 0,
  })

  const beamsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!beamsRef.current) return

      const rect = beamsRef.current.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      setMousePosition({ x, y })
    }

    document.addEventListener("mousemove", handleMouseMove)

    return () => {
      document.removeEventListener("mousemove", handleMouseMove)
    }
  }, [])

  const maskStyle = {
    "--x": `${mousePosition.x}px`,
    "--y": `${mousePosition.y}px`,
  } as React.CSSProperties

  return (
    <div
      ref={beamsRef}
      className={cn(
        "pointer-events-none fixed inset-0 z-0 h-full w-full bg-[#050A44] bg-opacity-70 opacity-60",
        className,
      )}
      style={maskStyle}
    >
      <div className="absolute inset-0 z-10 bg-transparent [mask-image:radial-gradient(circle_at_var(--x)_var(--y),transparent_30%,black_70%)]" />
      <div className="absolute left-0 right-0 bottom-0 top-0 z-0 bg-[radial-gradient(circle_500px_at_var(--x)_var(--y),#0A21C0_0%,transparent_80%)]" />
      <div className="absolute left-0 right-0 bottom-0 top-0 z-0 bg-[radial-gradient(circle_200px_at_var(--x)_var(--y),rgba(11,17,38,0.8)_0%,transparent_80%)]" />
    </div>
  )
}

