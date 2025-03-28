"use client"

import type React from "react"

import { useState } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Mail, Lock, Phone, Github } from "lucide-react"
import { BackgroundBeams } from "@/components/ui/background-beams"
import { toast } from "@/hooks/use-toast"

export default function AuthPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const initialMode = searchParams.get("mode") === "signup" ? "signup" : "signin"
  const [mode, setMode] = useState<"signin" | "signup">(initialMode)
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [phone, setPhone] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      // Simulate authentication
      await new Promise((resolve) => setTimeout(resolve, 1500))

      // In a real app, you would authenticate with Firebase here
      // For now, we'll just simulate a successful login

      // Store user info in localStorage
      localStorage.setItem("user", JSON.stringify({ email, isAuthenticated: true }))

      toast({
        title: mode === "signin" ? "Signed in successfully" : "Account created successfully",
        description: "Redirecting to upload page...",
      })

      // Redirect to upload page
      setTimeout(() => {
        router.push("/upload")
      }, 1000)
    } catch (error) {
      toast({
        title: "Authentication failed",
        description: "Please check your credentials and try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      <Navbar />
      <BackgroundBeams className="z-0" />

      <div className="container max-w-md mx-auto pt-20 px-4 relative z-10">
        <Card className="border-[#2C2E3A] backdrop-blur-sm bg-background/80">
          <CardHeader className="space-y-1 text-center">
            <CardTitle className="text-2xl">
              {mode === "signin" ? "Sign in to your account" : "Create an account"}
            </CardTitle>
            <CardDescription>
              {mode === "signin"
                ? "Enter your credentials to access your account"
                : "Fill in the details to create your account"}
            </CardDescription>
            <div className="flex items-center justify-center space-x-2 pt-4">
              <Label htmlFor="auth-mode">Sign In</Label>
              <Switch
                id="auth-mode"
                checked={mode === "signup"}
                onCheckedChange={(checked) => setMode(checked ? "signup" : "signin")}
              />
              <Label htmlFor="auth-mode">Sign Up</Label>
            </div>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="email"
                    placeholder="name@example.com"
                    type="email"
                    className="pl-10"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>

              {mode === "signup" && (
                <div className="space-y-2">
                  <Label htmlFor="phone">Phone Number</Label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="phone"
                      placeholder="+1 (555) 123-4567"
                      type="tel"
                      className="pl-10"
                      value={phone}
                      onChange={(e) => setPhone(e.target.value)}
                      required={mode === "signup"}
                    />
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="password"
                    placeholder="••••••••"
                    type="password"
                    className="pl-10"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
              </div>

              <Button type="submit" className="w-full bg-[#0A21C0] hover:bg-[#050A44]" disabled={isLoading}>
                {isLoading ? (
                  <span className="flex items-center">
                    <svg
                      className="animate-spin -ml-1 mr-3 h-4 w-4 text-white"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      ></path>
                    </svg>
                    {mode === "signin" ? "Signing In..." : "Signing Up..."}
                  </span>
                ) : mode === "signin" ? (
                  "Sign In"
                ) : (
                  "Sign Up"
                )}
              </Button>

              <div className="relative my-4">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">Or continue with</span>
                </div>
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full"
                onClick={() => {
                  toast({
                    title: "Google Sign In",
                    description: "This would connect to Google in a real implementation.",
                  })
                }}
              >
                <Github className="mr-2 h-4 w-4" />
                Google
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

