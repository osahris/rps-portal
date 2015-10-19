[[!meta title="Applying security updates"]]

Security updates provided by the distribution should be applied regularly (e.g. once per week).
For servers running Debian or Ubuntu, please do the following:

 * Login as a user with administrative rights.
 * Execute the following commands:

	sudo apt-get update

	sudo apt-get upgrade

The following software was not installed via the distribution's package system, therefore updates need to be applied manually:

 * (none so far)

(Please update this list when something new is installed out-of-band.)
For such software it is highly recommended that the administrator / administrative team are subscribed to the announcement mailing list of the respective projects, so that no updates which fix security bugs are missed.
