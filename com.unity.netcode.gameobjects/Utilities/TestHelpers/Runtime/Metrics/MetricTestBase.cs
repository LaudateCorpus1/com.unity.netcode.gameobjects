#if MULTIPLAYER_TOOLS
using System;
using System.Collections;
using UnityEngine;
using UnityEngine.TestTools;

namespace Unity.Netcode.TestHelpers.Runtime.Metrics
{
    internal abstract class SingleClientMetricTestBase : NetcodeIntegrationTest
    {
        protected override int NbClients => 1;

        protected virtual Action<GameObject> UpdatePlayerPrefab => _ => { };

        internal NetworkManager Server { get; private set; }

        internal NetworkMetrics ServerMetrics { get; private set; }

        internal NetworkManager Client { get; private set; }

        internal NetworkMetrics ClientMetrics { get; private set; }

        protected override IEnumerator OnPostSetup()
        {
            Server = m_ServerNetworkManager;
            ServerMetrics = Server.NetworkMetrics as NetworkMetrics;
            Client = m_ClientNetworkManagers[0];
            ClientMetrics = Client.NetworkMetrics as NetworkMetrics;
            return base.OnPreSetup();
        }
    }

    public abstract class DualClientMetricTestBase : NetcodeIntegrationTest
    {
        protected override int NbClients => 2;

        protected virtual Action<GameObject> UpdatePlayerPrefab => _ => { };

        internal NetworkManager Server { get; private set; }

        internal NetworkMetrics ServerMetrics { get; private set; }

        internal NetworkManager FirstClient { get; private set; }

        internal NetworkMetrics FirstClientMetrics { get; private set; }

        internal NetworkManager SecondClient { get; private set; }

        internal NetworkMetrics SecondClientMetrics { get; private set; }

        protected override IEnumerator OnPostSetup()
        {
            Server = m_ServerNetworkManager;
            ServerMetrics = Server.NetworkMetrics as NetworkMetrics;
            FirstClient = m_ClientNetworkManagers[0];
            FirstClientMetrics = FirstClient.NetworkMetrics as NetworkMetrics;
            SecondClient = m_ClientNetworkManagers[0];
            SecondClientMetrics = SecondClient.NetworkMetrics as NetworkMetrics;
            return base.OnPreSetup();
        }
    }
}
#endif