import { useEffect } from 'react'
import { useDeviceStore } from '../stores/deviceStore'
import { useWebSocket } from './useWebSocket'

export function useDevices() {
  const {
    ports,
    devices,
    selectedPort,
    loading,
    error,
    fetchPorts,
    fetchDevices,
    selectPort,
    connect,
    disconnect,
    setError,
  } = useDeviceStore()

  // Compute selected device from current state
  const selectedDevice = devices.find(d => d.port === selectedPort) ?? null

  const { subscribe, unsubscribe } = useWebSocket()

  // Fetch ports on mount
  useEffect(() => {
    fetchPorts()
    fetchDevices()
  }, [fetchPorts, fetchDevices])

  // Subscribe to selected device
  useEffect(() => {
    if (selectedPort) {
      subscribe(selectedPort)
      return () => unsubscribe(selectedPort)
    }
  }, [selectedPort, subscribe, unsubscribe])

  return {
    ports,
    devices,
    selectedPort,
    selectedDevice,
    loading,
    error,
    selectPort,
    connect,
    disconnect,
    refresh: fetchPorts,
    clearError: () => setError(null),
  }
}
