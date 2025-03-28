"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import Navbar from "@/components/navbar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, Upload, FileText, X, CheckCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { BackgroundGradient } from "@/components/ui/background-gradient"
import { toast } from "@/hooks/use-toast"
import { Progress } from "@/components/ui/progress"
import { AnimatedTooltip } from "@/components/ui/animated-tooltip"

export default function UploadPage() {
  const [files, setFiles] = useState<File[]>([])
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const router = useRouter()

  // Check authentication status
  useEffect(() => {
    const user = localStorage.getItem("user")
    if (user) {
      try {
        const userData = JSON.parse(user)
        setIsAuthenticated(userData.isAuthenticated)
      } catch (e) {
        setIsAuthenticated(false)
      }
    } else {
      setIsAuthenticated(false)
    }

    // If not authenticated, redirect after a short delay
    if (!isAuthenticated) {
      const timer = setTimeout(() => {
        router.push("/auth")
      }, 3000)

      return () => clearTimeout(timer)
    }
  }, [isAuthenticated, router])

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files).filter((file) => file.type === "application/pdf")
      setFiles((prev) => [...prev, ...newFiles])

      // Store files in IndexedDB
      if (newFiles.length > 0) {
        storeFilesInBrowser(newFiles)
      }
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    if (e.dataTransfer.files) {
      const newFiles = Array.from(e.dataTransfer.files).filter((file) => file.type === "application/pdf")
      setFiles((prev) => [...prev, ...newFiles])

      // Store files in IndexedDB
      if (newFiles.length > 0) {
        storeFilesInBrowser(newFiles)
      }
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  const storeFilesInBrowser = async (filesToStore: File[]) => {
    // For demonstration purposes, we'll just store file metadata in localStorage
    // In a real app, you would use IndexedDB for larger files
    try {
      const storedFiles = localStorage.getItem("storedPdfs")
        ? JSON.parse(localStorage.getItem("storedPdfs") || "[]")
        : []

      const newStoredFiles = [
        ...storedFiles,
        ...filesToStore.map((file) => ({
          name: file.name,
          size: file.size,
          type: file.type,
          lastModified: file.lastModified,
          // In a real app, you would store the file content in IndexedDB
        })),
      ]

      localStorage.setItem("storedPdfs", JSON.stringify(newStoredFiles))

      toast({
        title: "Files stored successfully",
        description: `${filesToStore.length} file(s) stored in browser storage.`,
      })
    } catch (error) {
      console.error("Error storing files:", error)
      toast({
        title: "Error storing files",
        description: "There was an error storing your files.",
        variant: "destructive",
      })
    }
  }

  const processFiles = () => {
    if (files.length === 0) return

    setIsUploading(true)
    setUploadProgress(0)

    // Simulate processing with progress
    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsUploading(false)
          toast({
            title: "Processing complete",
            description: `${files.length} file(s) processed successfully.`,
          })
          return 100
        }
        return prev + 5
      })
    }, 200)
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container max-w-4xl mx-auto pt-20 px-4">
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Authentication Required</AlertTitle>
            <AlertDescription>
              You need to sign in or sign up to access this feature. Redirecting you to the authentication page...
            </AlertDescription>
          </Alert>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <div className="container max-w-4xl mx-auto pt-20 px-4">
        <BackgroundGradient className="rounded-[22px] p-1 bg-gradient-to-r from-[#050A44] via-[#0A21C0] to-[#2C2E3A]">
          <Card className="w-full rounded-[20px] border-0">
            <CardHeader>
              <CardTitle className="text-2xl">Upload Resumes</CardTitle>
              <CardDescription>Upload PDF resumes to analyze with HireSense AI</CardDescription>
            </CardHeader>
            <CardContent>
              <div
                className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-10 text-center cursor-pointer hover:bg-muted/50 transition-colors relative overflow-hidden group"
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onClick={() => document.getElementById("file-upload")?.click()}
              >
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-2000 ease-in-out" />

                <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
                <h3 className="mt-4 text-lg font-semibold">Drag PDFs here or click to upload</h3>
                <p className="mt-2 text-sm text-muted-foreground">Only PDF files are supported</p>
                <input
                  id="file-upload"
                  type="file"
                  accept=".pdf"
                  multiple
                  className="hidden"
                  onChange={handleFileChange}
                />
              </div>

              {files.length > 0 && (
                <div className="mt-6">
                  <h4 className="font-medium mb-2">Uploaded Files ({files.length})</h4>
                  <ul className="space-y-2">
                    {files.map((file, index) => (
                      <li
                        key={index}
                        className="p-3 bg-muted rounded-lg flex justify-between items-center group hover:bg-muted/80 transition-colors"
                      >
                        <div className="flex items-center">
                          <FileText className="h-5 w-5 mr-2 text-[#0A21C0]" />
                          <span className="truncate max-w-[200px] md:max-w-[400px]">{file.name}</span>
                        </div>
                        <div className="flex items-center">
                          <span className="text-xs text-muted-foreground mr-4">{(file.size / 1024).toFixed(1)} KB</span>
                          <AnimatedTooltip content="Remove file">
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                              onClick={(e) => {
                                e.stopPropagation()
                                removeFile(index)
                              }}
                            >
                              <X className="h-4 w-4" />
                            </Button>
                          </AnimatedTooltip>
                        </div>
                      </li>
                    ))}
                  </ul>

                  {isUploading && (
                    <div className="mt-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span>Processing files...</span>
                        <span>{uploadProgress}%</span>
                      </div>
                      <Progress value={uploadProgress} className="h-2" />
                    </div>
                  )}

                  <Button
                    className="mt-4 w-full bg-[#0A21C0] hover:bg-[#050A44] relative overflow-hidden group"
                    onClick={processFiles}
                    disabled={isUploading}
                  >
                    <span className="relative z-10 flex items-center">
                      {isUploading ? (
                        <>
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
                          Processing...
                        </>
                      ) : (
                        <>
                          <CheckCircle className="mr-2 h-4 w-4" />
                          Process Files
                        </>
                      )}
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out" />
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </BackgroundGradient>
      </div>
    </div>
  )
}

