/*
   Copyright 2020 Docker Compose CLI authors

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

package main

import (
	"context"
	"log"
	"os"

	dockercli "github.com/docker/cli/cli"
	"github.com/docker/cli/cli-plugins/manager"
	"github.com/docker/cli/cli-plugins/plugin"
	"github.com/docker/cli/cli/command"
	"github.com/spf13/cobra"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"

	"github.com/docker/compose/v2/cmd/compatibility"
	commands "github.com/docker/compose/v2/cmd/compose"
	"github.com/docker/compose/v2/internal"
	"github.com/docker/compose/v2/pkg/api"
	"github.com/docker/compose/v2/pkg/compose"
	"github.com/docker/compose/v2/pkg/utils"
)

func pluginMain() {
	plugin.Run(func(dockerCli command.Cli) *cobra.Command {
		tracingShutdown, err := commands.InitProvider()
		if err != nil {
			log.Fatal(err)
		}
		var cmdSpan trace.Span

		serviceProxy := api.NewServiceProxy().WithService(compose.NewComposeService(dockerCli, utils.Tracer))
		cmd := commands.RootCommand(dockerCli, serviceProxy)
		originalPreRun := cmd.PersistentPreRunE
		cmd.PersistentPreRunE = func(cmd *cobra.Command, args []string) error {
			ctx := cmd.Context()
			ctx, cmdSpan = utils.Tracer.Start(ctx, "CLICommand",
				trace.WithAttributes(
					attribute.String("cmd", cmd.Name())))
			cmd.SetContext(ctx)
			if err := plugin.PersistentPreRunE(cmd, args); err != nil {
				return err
			}
			if originalPreRun != nil {
				return originalPreRun(cmd, args)
			}
			return nil
		}
		originalPostRun := cmd.PersistentPostRunE
		cmd.PersistentPostRunE = func(cmd *cobra.Command, args []string) error {
			var err error
			if originalPostRun != nil {
				err = originalPostRun(cmd, args)
			}
			if cmdSpan != nil {
				cmdSpan.End()
			}
			if err := tracingShutdown(context.Background()); err != nil {
				log.Fatal(err)
			}
			return err
		}
		cmd.SetFlagErrorFunc(func(c *cobra.Command, err error) error {
			return dockercli.StatusError{
				StatusCode: compose.CommandSyntaxFailure.ExitCode,
				Status:     err.Error(),
			}
		})
		return cmd
	},
		manager.Metadata{
			SchemaVersion: "0.1.0",
			Vendor:        "Docker Inc.",
			Version:       internal.Version,
		})
}

func main() {
	if plugin.RunningStandalone() {
		os.Args = append([]string{"docker"}, compatibility.Convert(os.Args[1:])...)
	}
	pluginMain()
}
