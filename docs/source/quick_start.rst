Quick Start
===========
You use the capabilities of Quipucords to inspect and gather information on your IT infrastructure. The following information describes how you use the qpc command line interface to complete a simple Quipucords task of scanning a network and viewing a report. The complete list of options for each qpc command and subcommand are listed in the `qpc man page <man.html>`_.

Quipucords requires the configuration of two basic structures to manage the inspection process. A *credential* contains the access credentials, such as the user name and password or SSH key of the user, with sufficient authority to run the inspection process on a particular source. For more information about this authority, see `Requirements <requirements.html>`_. A *source* defines the entity or entities to be inspected, such as a host, subnet, network, or systems management solution such as vCenter Server or Satellite. When you create a source, you also include one or more of the configured credentials to use to access the individual entities in the source during the inspection process.

You can save multiple credentials and sources to use with Quipucords in various combinations as you run inspection processes, or *scans*. When you have completed a scan, you can access the collection of *facts* in the output as a *report* to review the results.

Before You Begin: Check Setup and Connection to the Quipucords Server
---------------------------------------------------------------------

Setup of the Quipucords Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you have not already setup your Quipucords server refer to the `Installing and Configuring Quipucords <install.html>`_ documentation first.

Connection to the Quipucords Server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In some organizations, a single person might be responsible for scanning IT resources. However, in others, multiple people might hold this responsibility. Any additional Quipucords users who did not install the Quipucords server and command line tool must ensure that the command line tool instance is configured to connect to the server and that the user name can log in to the command line interface.

For more information, see the following sections:

- `Configuring the qpc Command Line Tool Connection <install.html#connection>`_
- `Logging in to the Quipucords Server <install.html#login>`_.

Creating Credentials and Sources for a Network
----------------------------------------------

A *network* source is composed of one or more host names, one or more IP addresses, IP ranges, or a combination of these network resources. In addition, the source creation command references one or more credentials. Typically, a network source might include multiple credentials because it is expected that many credentials would be needed to access a broad IP range.

The following scenario provide examples of how you would create a network source and credentials.

To create a network source, use the following steps:

1. Create a network credential with root-level access::

   # qpc cred add --type network --name cred_name --username root_name [--sshkeyfile key_file] [--password]

   If you did not use the ``sshkeyfile`` option to provide an SSH key for the user name value, enter the password of the user with root-level access at the connection password prompt. See the section on `Working with Credentials and Sources <working_with_sources.html>`_ for further details.

   For example, for a network credential where the credential name is ``sudouser1``, the user with root-level access is ``sysadmin``, and the access is obtained through the password option, you would enter the following command::

   # qpc cred add --type network --name sudouser1 --username sysadmin --password --become-password

   After you enter this command, you are prompted to enter two passwords. First, you would enter the connection password for the ``username`` user, and then you would enter the password for the ``become-method``, which is the ``sudo`` command by default.

2. Create a network source that specifies one or more network identifiers, such as a host name or host names, an IP address, a list of IP addresses, or an IP range, and one or more network credentials to be used for the scan.

   **TIP:** You can provide IP range values in CIDR or Ansible notation.

   ::

   # qpc source add --type network --name source_name --hosts host_name_or_file --cred cred_name

   For example, for a network source where the source name is ``mynetwork``, the network to be scanned is the ``192.0.2.0/24`` subnet, and the network credentials that are used to run the scan are ``roothost1`` and ``roothost2``, you would enter the following command::

   # qpc source add --type network --name mynetwork --hosts 192.0.2.[1:254] --cred roothost1 roothost2

   See the section on `Working with Credentials and Sources <working_with_sources.html>`_ for further details.

Creating a Scan
---------------
After you set up your credentials and sources, you can run a Quipucords scan to inspect your IT environment. You can create a scan on a single source or combine sources, even sources of different types.

To create a scan, use the following steps:

Create the scan by using the ``scan add`` command, specifying a name for the ``name`` option and one or more sources for the ``sources`` option::

  # qpc scan add --name scan1 --sources source_name1 source_name2

For example, if you want to create a scan called ``myscan`` with the network source, you would enter the following command::

  # qpc scan add --name myscan --sources mynetwork

For more information on viewing, editing or review scans refer to the `Working with Scans <working_with_scans.html>`_ section.

Running a Scan
--------------
To run a scan, use the following steps:

Run the scan by using the ``scan start`` command, specifying the name of a scan for the ``name`` option::

  # qpc scan start --name scan_name1

For example, if you want to run the scan ``myscan``, you would enter the following command::

  # qpc scan start --name myscan


When you run the ``scan start`` command, the output provides an identifier for that scan job. You can show the scan job results to follow the status of the scan job, see the `Working with Scan Jobs <working_with_scan_jobs.html>`_ section for further details.

Viewing the Scan Report
-----------------------
When the scan job completes, you have the capability to produce a report for that scan job. You can request a report with all the details, or facts, of the scan, or request a report with a summary. The summary report process runs steps to merge the facts found during the inspection of the various hosts that are contacted during the scan. When possible, the report process also runs steps to deduplicate redundant systems. For both types of reports, you can produce the report in JavaScript Object Notation (JSON) format or comma-separated values (CSV) format.

To generate a summary report, enter the ``report summary`` command and specify the identifier for the scan job and the format for the output file.

For example, if you want to create the report summary for a scan with the scan job identifier of ``1`` and you want to generate that report in CSV format in the ``~/scan_result.csv`` file, you would enter the following command::

  # qpc report summary --scan-job 1 --csv --output-file=~/scan_result.csv

However, if you want to create the detailed report, you would use the ``report detail`` command.  This command takes the same options as the ``report summary`` command. The output is not deduplicated and merged, so it contains all facts from each source. For example, to create the detailed report for a scan with the scan job identifier ``1``, with CSV output in the ``~/scan_result.csv`` file, you would enter the following command::

  # qpc report detail --scan-job 1 --csv --output-file=~/scan_result.csv

For further details on creating a report from multiple scan job results see the `Working with Reports <working_with_reports.html>`_ section.
