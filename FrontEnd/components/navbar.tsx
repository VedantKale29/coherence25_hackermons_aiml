"use client"

import { useState } from "react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { MoonIcon, SunIcon } from "lucide-react"
import { useTheme } from "next-themes"

export default function Navbar() {
  const { theme, setTheme } = useTheme()
  const [isContactOpen, setIsContactOpen] = useState(false)

  return (
    <nav className="relative z-20 w-full py-4 px-6 md:px-12 flex items-center justify-between">
      <Link href="/" className="text-2xl font-bold text-white">
        HireSense AI
      </Link>

      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
          className="text-white hover:text-white hover:bg-white/10"
        >
          {theme === "dark" ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
          <span className="sr-only">Toggle theme</span>
        </Button>

        <Popover open={isContactOpen} onOpenChange={setIsContactOpen}>
          <PopoverTrigger asChild>
            <Button
              variant="ghost"
              className="text-white hover:text-white hover:bg-white/10"
              onMouseEnter={() => setIsContactOpen(true)}
              onMouseLeave={() => setIsContactOpen(false)}
            >
              Contact Us
            </Button>
          </PopoverTrigger>
          <PopoverContent
            className="w-80 bg-[#2C2E3A] border-[#141619] text-white"
            onMouseEnter={() => setIsContactOpen(true)}
            onMouseLeave={() => setIsContactOpen(false)}
          >
            <div className="space-y-2">
              <h4 className="font-medium text-lg">Contact Information</h4>
              <div className="grid gap-1">
                <p className="text-sm">Email: contact@hiresense.ai</p>
                <p className="text-sm">Phone: +1 (555) 123-4567</p>
              </div>
            </div>
          </PopoverContent>
        </Popover>

        <Link href="/auth">
          <Button variant="outline" className="text-white border-white hover:bg-white/10">
            Sign In
          </Button>
        </Link>

        <Link href="/auth?mode=signup">
          <Button className="bg-[#0A21C0] hover:bg-[#050A44] text-white">Sign Up</Button>
        </Link>
      </div>
    </nav>
  )
}

