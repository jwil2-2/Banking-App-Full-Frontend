function StatusBanner({ message, messageType }) {
  if (!message) {
    return null
  }

  return <section className={messageType === 'error' ? 'message error' : 'message success'}>{message}</section>
}

export default StatusBanner
