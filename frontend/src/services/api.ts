/**
 * API client for Pulsar backend
 */

const API_BASE = '/api'

interface ApiResponse<T> {
  data?: T
  error?: string
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    })

    const data = await response.json()

    if (!response.ok) {
      return { error: data.error || `HTTP ${response.status}` }
    }

    return { data }
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'Network error' }
  }
}

// Port operations
export const api = {
  // Generic methods for LSP and other services
  get: <T>(endpoint: string) => request<T>(endpoint),
  post: <T>(endpoint: string, body?: unknown) =>
    request<T>(endpoint, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    }),

  // Ports
  getPorts: () => request<PortInfo[]>('/ports'),

  // Devices
  getDevices: () => request<DeviceInfo[]>('/devices'),
  getDevice: (port: string) => request<DeviceInfo>(`/devices/${encodeURIComponent(port)}`),
  connect: (port: string, baudrate?: number) =>
    request<{ success: boolean; device: DeviceInfo }>(
      `/devices/${encodeURIComponent(port)}/connect`,
      {
        method: 'POST',
        body: JSON.stringify({ baudrate }),
      }
    ),
  disconnect: (port: string) =>
    request<{ success: boolean }>(`/devices/${encodeURIComponent(port)}/disconnect`, {
      method: 'POST',
    }),
  reset: (port: string, soft = true) =>
    request<{ success: boolean }>(`/devices/${encodeURIComponent(port)}/reset`, {
      method: 'POST',
      body: JSON.stringify({ soft }),
    }),
  interrupt: (port: string) =>
    request<{ success: boolean }>(`/devices/${encodeURIComponent(port)}/interrupt`, {
      method: 'POST',
    }),

  // REPL
  execute: (port: string, code: string, timeout = 30) =>
    request<REPLResult>(`/devices/${encodeURIComponent(port)}/repl`, {
      method: 'POST',
      body: JSON.stringify({ code, timeout }),
    }),

  // Files
  listFiles: (port: string, path = '/') =>
    request<FileInfo[]>(`/devices/${encodeURIComponent(port)}/files?path=${encodeURIComponent(path)}`),
  readFile: (port: string, path: string) =>
    request<{ content: string; binary: boolean }>(
      `/devices/${encodeURIComponent(port)}/files/read?path=${encodeURIComponent(path)}`
    ),
  writeFile: (port: string, path: string, content: string, binary = false) =>
    request<{ success: boolean }>(`/devices/${encodeURIComponent(port)}/files/write`, {
      method: 'POST',
      body: JSON.stringify({ path, content, binary }),
    }),
  deleteFile: (port: string, path: string) =>
    request<{ success: boolean }>(
      `/devices/${encodeURIComponent(port)}/files?path=${encodeURIComponent(path)}`,
      { method: 'DELETE' }
    ),
  mkdir: (port: string, path: string) =>
    request<{ success: boolean }>(`/devices/${encodeURIComponent(port)}/files/mkdir`, {
      method: 'POST',
      body: JSON.stringify({ path }),
    }),

  // Firmware
  listFirmware: () => request<FirmwareInfo[]>('/firmware/list'),
  flashFirmware: (port: string, firmwarePath: string) =>
    request<{ success: boolean }>('/firmware/flash', {
      method: 'POST',
      body: JSON.stringify({ port, firmware_path: firmwarePath }),
    }),
  getFirmwareProgress: () => request<FlashProgress>('/firmware/progress'),

  // WiFi
  scanWifi: (port: string) =>
    request<WifiNetwork[]>(`/devices/${encodeURIComponent(port)}/wifi/scan`),
  configureWifi: (port: string, ssid: string, password: string) =>
    request<{ success: boolean }>(`/devices/${encodeURIComponent(port)}/wifi/config`, {
      method: 'POST',
      body: JSON.stringify({ ssid, password }),
    }),
  getWifiStatus: (port: string) =>
    request<WifiStatus>(`/devices/${encodeURIComponent(port)}/wifi/status`),

  // Chip Info (esptool)
  getChipInfo: (port: string) =>
    request<ChipInfo>(`/devices/${encodeURIComponent(port)}/chipinfo`),

  // Firmware additional
  eraseFirmware: (port: string) =>
    request<{ success: boolean }>('/firmware/erase', {
      method: 'POST',
      body: JSON.stringify({ port }),
    }),

  // Folder Sync
  syncCompare: (port: string, folder: string, remote = '/') =>
    request<SyncCompareResult>(`/devices/${encodeURIComponent(port)}/sync/compare`, {
      method: 'POST',
      body: JSON.stringify({ folder, remote }),
    }),
  syncUpload: (port: string, folder: string, remote = '/', dryRun = false) =>
    request<SyncResult>(`/devices/${encodeURIComponent(port)}/sync/upload`, {
      method: 'POST',
      body: JSON.stringify({ folder, remote, dry_run: dryRun }),
    }),
}

// Type definitions
export interface PortInfo {
  port: string
  description: string
  hwid: string
  vid: number | null
  pid: number | null
  manufacturer: string | null
  product: string | null
  serial_number: string | null
}

export interface DeviceInfo {
  port: string
  baudrate: number
  state: 'disconnected' | 'connecting' | 'connected' | 'busy' | 'error'
  firmware: string
  machine: string
  platform: string
  connected_at: string | null
  error: string
}

export interface REPLResult {
  output: string
  error: string
  success: boolean
}

export interface FileInfo {
  name: string
  path: string
  is_dir: boolean
  size: number
}

export interface FirmwareInfo {
  name: string
  path?: string
  url?: string
  chip?: string
  size?: number
  local: boolean
}

export interface FlashProgress {
  status: 'idle' | 'starting' | 'erasing' | 'erased' | 'flashing' | 'downloading' | 'downloaded' | 'complete' | 'error'
  progress: number
  message: string
  error: string
}

export interface WifiNetwork {
  ssid: string
  bssid: string
  channel: number
  rssi: number
  authmode: string
  hidden: boolean
  signal: 'excellent' | 'good' | 'fair' | 'weak'
}

export interface WifiStatus {
  connected: boolean
  ssid: string
  ip: string
  netmask: string
  gateway: string
  dns: string
  mac: string
}

export interface ChipInfo {
  chip: string
  chip_id: string
  mac_address: string
  flash_size: string
  flash_type: string
  crystal: string
  features: string[]
  raw_output: string
}

export interface SyncFile {
  path: string
  size: number
  local_hash: string | null
  remote_hash: string | null
  needs_upload: boolean
}

export interface SyncCompareResult {
  files: SyncFile[]
  to_upload: string[]
  total: number
  needs_upload: number
}

export interface SyncResult {
  uploaded: string[]
  failed: string[]
  skipped: string[]
  errors: string[]
  success: boolean
}
