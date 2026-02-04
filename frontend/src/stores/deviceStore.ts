import { create } from 'zustand'
import { api, DeviceInfo, PortInfo } from '../services/api'

// Selector to get selected device (use with useDeviceStore)
export const selectSelectedDevice = (state: DeviceState): DeviceInfo | null => {
  return state.devices.find(d => d.port === state.selectedPort) ?? null
}

interface DeviceState {
  ports: PortInfo[]
  devices: DeviceInfo[]
  selectedPort: string | null
  loading: boolean
  error: string | null

  // Actions
  fetchPorts: () => Promise<void>
  fetchDevices: () => Promise<void>
  selectPort: (port: string | null) => void
  connect: (port: string, baudrate?: number) => Promise<boolean>
  disconnect: (port: string) => Promise<void>
  updateDevice: (device: Partial<DeviceInfo> & { port: string }) => void
  removeDevice: (port: string) => void
  setError: (error: string | null) => void
  getSelectedDevice: () => DeviceInfo | null
}

export const useDeviceStore = create<DeviceState>((set, get) => ({
  ports: [],
  devices: [],
  selectedPort: null,
  loading: false,
  error: null,

  // Get selected device - call this as a function
  getSelectedDevice: () => {
    const state = get()
    return state.devices.find(d => d.port === state.selectedPort) ?? null
  },

  fetchPorts: async () => {
    set({ loading: true, error: null })
    const result = await api.getPorts()
    if (result.error) {
      set({ error: result.error, loading: false })
    } else {
      set({ ports: result.data ?? [], loading: false })
    }
  },

  fetchDevices: async () => {
    const result = await api.getDevices()
    if (result.data) {
      set({ devices: result.data })
    }
  },

  selectPort: (port) => {
    set({ selectedPort: port })
  },

  connect: async (port, baudrate) => {
    console.log('[DeviceStore] Connecting to:', port)
    set({ loading: true, error: null })
    const result = await api.connect(port, baudrate)

    console.log('[DeviceStore] Connect result:', JSON.stringify(result, null, 2))

    if (result.error) {
      console.log('[DeviceStore] Connect error:', result.error)
      set({ error: result.error, loading: false })
      return false
    }

    if (result.data?.device) {
      console.log('[DeviceStore] Device connected:', result.data.device)
      set(state => {
        const newDevices = [...state.devices.filter(d => d.port !== port), result.data!.device]
        console.log('[DeviceStore] New devices list:', newDevices)
        return {
          devices: newDevices,
          selectedPort: port,
          loading: false,
        }
      })
      return true
    }

    console.log('[DeviceStore] No device in response, result.data:', result.data)
    set({ loading: false })
    return false
  },

  disconnect: async (port) => {
    await api.disconnect(port)
    set(state => ({
      devices: state.devices.filter(d => d.port !== port),
      selectedPort: state.selectedPort === port ? null : state.selectedPort,
    }))
  },

  updateDevice: (update) => {
    set(state => ({
      devices: state.devices.map(d =>
        d.port === update.port ? { ...d, ...update } : d
      ),
    }))
  },

  removeDevice: (port) => {
    set(state => ({
      devices: state.devices.filter(d => d.port !== port),
      selectedPort: state.selectedPort === port ? null : state.selectedPort,
    }))
  },

  setError: (error) => {
    set({ error })
  },
}))
