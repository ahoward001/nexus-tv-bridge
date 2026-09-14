"""BabyMon -- a local-only baby monitor.

Design rule, enforced throughout this package: audio and video are processed
in memory on this machine and are never written to disk, never uploaded, and
never sent to any AI service. What leaves this laptop is an event -- a short
line of text saying something happened -- and, only if you enable the stream,
live frames over an encrypted tailnet to your own phone.
"""

__version__ = "1.0.0"
