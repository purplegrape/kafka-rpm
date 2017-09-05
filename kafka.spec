Name:           kafka
Version:        0.11.0.0
Release:        2%{?dist}
Group:          Applications/Internet
License:        Apache (v2)
Vendor:         Apache Software Foundation
URL:            http://kafka.apache.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
Summary:        Kafka is a distributed publish/subscribe messaging system

Source0:        kafka_2.12-%{version}.tgz
Source1:        kafka.ini
Source2:        zookeeper.ini

Requires:       java >= 1.7
Requires:       supervisor
Requires(pre):  shadow-utils

%description
It is designed to support the following

Persistent messaging with O(1) disk structures that provide constant time performance even with many TB of stored messages.
High-throughput: even with very modest hardware Kafka can support hundreds of thousands of messages per second.
Explicit support for partitioning messages over Kafka servers and distributing consumption over a cluster of consumer machines while maintaining per-partition ordering semantics.
Support for parallel data load into Hadoop.
Kafka is aimed at providing a publish-subscribe solution that can handle all activity stream data and processing on a consumer-scale web site. This kind of activity (page views, searches, and other user actions) are a key ingredient in many of the social feature on the modern web. This data is typically handled by "logging" and ad hoc log aggregation solutions due to the throughput requirements. This kind of ad hoc solution is a viable solution to providing logging data to an offline analysis system like Hadoop, but is very limiting for building real-time processing. Kafka aims to unify offline and online processing by providing a mechanism for parallel load into Hadoop as well as the ability to partition real-time consumption over a cluster of machines.

See our web site for more details on the project. (http://kafka.apache.org/)

%prep

%setup -n %{name}_2.12-%{version}


%build

%install

rm -rf $RPM_BUILD_ROOT

%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/%{name}
%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/kafka
%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}

%{__cp} -a config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

%{__cp} -R bin $RPM_BUILD_ROOT%{_datadir}/%{name}/
%{__cp} -R libs $RPM_BUILD_ROOT%{_datadir}/%{name}/

rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/bin/windows

%{__mkdir_p} $RPM_BUILD_ROOT%{_sysconfdir}/supervisord.d
%{__install} -m 644  %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/supervisord.d/kafka.ini
%{__install} -m 644  %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/supervisord.d/zookeeper.ini

#fix zookeeper default data dir
%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/zookeeper
sed -i 's#/tmp/zookeeper#/var/lib/kafka/zookeeper#g' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zookeeper.properties

#fix kafka default data dir
%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/data
sed -i 's#/tmp/kafka-logs#/var/lib/kafka/data#g' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/server.properties

#fix kafka default log dir,see /etc/supervisor.d/kafka.ini
%{__mkdir_p} $RPM_BUILD_ROOT%{_sharedstatedir}/%{name}/logs


%clean
rm -rf $RPM_BUILD_ROOT

%pre

# Create user and group
getent group  kafka >/dev/null || groupadd -r kafka
getent passwd kafka >/dev/null || useradd -r -g kafka -d /var/lib/kafka -s /bin/nologin kafka

exit 0

%post

ln -sf /var/lib/kafka /usr/share/kafka/logs
ln -sf /etc/kafka /usr/share/kafka/config

%preun
supervisorctl stop kafka || true
supervisorctl stop zookeeper || true

%files
%defattr(-,kafka,kafka)
%{_datadir}/%{name}
%{_sharedstatedir}/kafka

%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.properties

%{_sysconfdir}/supervisord.d/kafka.ini
%{_sysconfdir}/supervisord.d/zookeeper.ini

%license LICENSE
%doc NOTICE

%changelog
* Thu Aug 10 2017 Purple Grape <purplegrape4@gmail.com>
- init 0.11.0.0
