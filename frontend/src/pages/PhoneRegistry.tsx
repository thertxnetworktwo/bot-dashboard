import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { toast } from 'sonner'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { api } from '@/lib/api'

export default function PhoneRegistry() {
  const [phoneNumber, setPhoneNumber] = useState('')
  const [bulkNumbers, setBulkNumbers] = useState('')

  const checkMutation = useMutation({
    mutationFn: api.phone.check,
    onSuccess: (data) => {
      if (data.exists) {
        toast.success(`Phone number ${data.phone_number} exists in registry`)
      } else {
        toast.info(`Phone number ${data.phone_number} not found in registry`)
      }
    },
  })

  const registerMutation = useMutation({
    mutationFn: api.phone.register,
    onSuccess: (data) => {
      if (data.success) {
        toast.success(`Phone number ${data.phone_number} registered successfully`)
        setPhoneNumber('')
      } else {
        toast.error(data.message || 'Failed to register phone number')
      }
    },
  })

  const bulkRegisterMutation = useMutation({
    mutationFn: ({ numbers }: { numbers: string[] }) => api.phone.bulkRegister(numbers),
    onSuccess: (data) => {
      if (data.success) {
        toast.success(`Successfully registered ${data.registered_count} phone numbers`)
        setBulkNumbers('')
      } else {
        toast.error(`Failed to register ${data.failed_count} phone numbers`)
      }
    },
  })

  const cleanupMutation = useMutation({
    mutationFn: api.phone.cleanup,
    onSuccess: (data) => {
      if (data.success) {
        toast.success(`Cleanup completed. Deleted ${data.deleted_count} records`)
      } else {
        toast.error(data.message || 'Cleanup failed')
      }
    },
  })

  const handleBulkRegister = () => {
    const numbers = bulkNumbers
      .split('\n')
      .map(n => n.trim())
      .filter(n => n.length > 0)
    
    if (numbers.length === 0) {
      toast.error('Please enter at least one phone number')
      return
    }
    
    if (numbers.length > 1000) {
      toast.error('Maximum 1000 phone numbers allowed')
      return
    }
    
    bulkRegisterMutation.mutate({ numbers })
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Phone Registry</h1>
        <p className="text-gray-500 mt-1">Manage phone number registry</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Check Phone Number</CardTitle>
            <CardDescription>Check if a phone number exists in the registry</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="check-phone">Phone Number</Label>
              <Input
                id="check-phone"
                type="tel"
                placeholder="+1234567890"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </div>
            <Button
              onClick={() => phoneNumber && checkMutation.mutate(phoneNumber)}
              disabled={!phoneNumber || checkMutation.isPending}
            >
              Check
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Register Phone Number</CardTitle>
            <CardDescription>Register a single phone number</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="register-phone">Phone Number</Label>
              <Input
                id="register-phone"
                type="tel"
                placeholder="+1234567890"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </div>
            <Button
              onClick={() => phoneNumber && registerMutation.mutate(phoneNumber)}
              disabled={!phoneNumber || registerMutation.isPending}
            >
              Register
            </Button>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Bulk Register</CardTitle>
          <CardDescription>Register up to 1000 phone numbers at once (one per line)</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="bulk-numbers">Phone Numbers</Label>
            <textarea
              id="bulk-numbers"
              className="w-full min-h-[200px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
              placeholder="+1234567890&#10;+0987654321&#10;..."
              value={bulkNumbers}
              onChange={(e) => setBulkNumbers(e.target.value)}
            />
          </div>
          <Button
            onClick={handleBulkRegister}
            disabled={!bulkNumbers || bulkRegisterMutation.isPending}
          >
            Bulk Register
          </Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Cleanup Old Records</CardTitle>
          <CardDescription>Remove old phone records from the registry</CardDescription>
        </CardHeader>
        <CardContent>
          <Button
            variant="destructive"
            onClick={() => {
              if (confirm('Are you sure you want to cleanup old records?')) {
                cleanupMutation.mutate()
              }
            }}
            disabled={cleanupMutation.isPending}
          >
            Cleanup
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
