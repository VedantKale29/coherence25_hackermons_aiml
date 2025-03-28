"use client"
import { useEffect, useState } from "react"
import { cn } from "@/lib/utils"

export const TextGenerateEffect = ({
  words,
  className,
}: {
  words: string
  className?: string
}) => {
  const [displayedText, setDisplayedText] = useState("")
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isComplete, setIsComplete] = useState(false)

  useEffect(() => {
    if (currentIndex < words.length) {
      const timeout = setTimeout(() => {
        setDisplayedText((prev) => prev + words[currentIndex])
        setCurrentIndex((prev) => prev + 1)
      }, 30) // Adjust speed as needed

      return () => clearTimeout(timeout)
    } else {
      setIsComplete(true)
    }
  }, [currentIndex, words])

  return (
    <div className={cn("", className)}>
      <p
        className={cn(
          "text-base sm:text-xl",
          isComplete ? "after:content-['']" : "after:content-['|'] after:animate-blink",
        )}
      >
        {displayedText}
      </p>
    </div>
  )
}

