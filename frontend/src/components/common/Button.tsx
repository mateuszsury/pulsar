import { ButtonHTMLAttributes, forwardRef } from 'react'

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'default'
  size?: 'xs' | 'sm' | 'md' | 'lg'
  icon?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'secondary', size = 'md', icon, className = '', children, ...props }, ref) => {
    const baseClasses = 'inline-flex items-center justify-center font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed'

    const variantClasses = {
      primary: 'bg-vscode-button text-white hover:bg-vscode-button-hover',
      secondary: 'bg-vscode-input text-vscode-text hover:bg-vscode-hover',
      ghost: 'bg-transparent text-vscode-text hover:bg-vscode-hover',
      danger: 'bg-vscode-error/20 text-vscode-error hover:bg-vscode-error/30',
      default: 'bg-vscode-accent/20 text-vscode-accent hover:bg-vscode-accent/30',
    }

    const sizeClasses = icon
      ? {
          xs: 'p-0.5',
          sm: 'p-1',
          md: 'p-1.5',
          lg: 'p-2',
        }
      : {
          xs: 'px-1 py-0.5 text-xs rounded',
          sm: 'px-2 py-1 text-xs rounded',
          md: 'px-3 py-1.5 text-sm rounded',
          lg: 'px-4 py-2 text-base rounded',
        }

    return (
      <button
        ref={ref}
        className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${icon ? 'rounded' : ''} ${className}`}
        {...props}
      >
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
